#!/usr/bin/env python3
"""
Agente Guardian — Motor de Nómina Pro (Universidad de Caldas)
LangChain + Llama 3 8B (Ollama) → genera Pytest → ejecuta en Sandbox.
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent

# ─── CONFIGURACIÓN DE RUTAS ───────────────────────────────────────────────────
MODEL        = "llama3.1:8b" # C1: Conecta con el modelo local
BASE_DIR     = Path(__file__).resolve().parent.parent
CASOS_FILE   = BASE_DIR / "casos_prueba.md"
ENGINE_FILE  = BASE_DIR / "src" / "engine.py"
TESTS_FILE   = BASE_DIR / "tests" / "test_generated.py"
SANDBOX_FILE = BASE_DIR / "guardian" / "sandbox.py"
VERDICT_FILE = BASE_DIR / "veredicto.json"

llm = ChatOllama(model=MODEL, temperature=0)

# ─── TOOLS ────────────────────────────────────────────────────────────────────

@tool
def leer_contexto_proyecto() -> str:
    """Lee casos_prueba.md y src/engine.py para entender las reglas R1 a R5."""
    if not CASOS_FILE.exists() or not ENGINE_FILE.exists():
        return "ERROR: Faltan archivos base (casos_prueba.md o src/engine.py)."
    
    casos = CASOS_FILE.read_text(encoding="utf-8")
    codigo = ENGINE_FILE.read_text(encoding="utf-8")
    return f"--- ORÁCULO ---\n{casos}\n\n--- CÓDIGO FUENTE ---\n{codigo}"

@tool
def guardar_tests(codigo: str) -> str:
    """
    Escribe el codigo Python/Pytest recibido en tests/test_generated.py.
    Debe importar liquidar_nomina desde src.engine y cubrir las reglas R1 a R5.
    """
    TESTS_FILE.parent.mkdir(exist_ok=True)
    # Limpieza defensiva de markdown
    codigo_limpio = codigo.replace("```python", "").replace("```", "").strip()
    TESTS_FILE.write_text(codigo_limpio, encoding="utf-8")
    return f"test_generated.py guardado en la carpeta tests/."

@tool
def ejecutar_sandbox_docker() -> str:
    """
    Invoca el script guardian/sandbox.py que levanta Docker, ejecuta pytest
    y devuelve el reporte de fallos y el veredicto final.
    """
    if not SANDBOX_FILE.exists():
        return "ERROR: sandbox.py no existe."
        
    resultado = subprocess.run(
        ["python", str(SANDBOX_FILE)],
        capture_output=True,
        text=True,
        cwd=str(BASE_DIR)
    )
    return resultado.stdout if resultado.stdout else resultado.stderr

@tool
def guardar_veredicto_auditoria(resumen: str) -> str:
    """Guarda el veredicto final en veredicto.json con metadatos."""
    payload = {
        "timestamp": datetime.now().isoformat(),
        "modelo_ia": MODEL,
        "tests_generados": str(TESTS_FILE),
        "resumen_agente": resumen,
    }
    VERDICT_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return f"Veredicto auditable guardado en {VERDICT_FILE.name}"

# ─── PROMPT DEL AGENTE ────────────────────────────────────────────────────────

SYSTEM_PROMPT = """Eres el Agente Guardian de QA. Tu misión es ejecutar este flujo en orden:

PASO 1 — Leer contexto
  Usa leer_contexto_proyecto para obtener las reglas R1-R5 y el motor de nómina.

PASO 2 — Generar código Pytest
  Analiza los casos y genera pruebas con @pytest.mark.parametrize que:
  - Importen: from src.engine import liquidar_nomina
  - Cubran las reglas R1 a R5 separando casos válidos y excepciones (ValueError).
  Usa guardar_tests para escribir el código. No uses texto markdown.

PASO 3 — Ejecutar Sandbox
  Usa ejecutar_sandbox_docker para delegar la construcción de la imagen y ejecución aislada.

PASO 4 — Guardar veredicto auditable
  Analiza el JSON devuelto por el Sandbox y usa guardar_veredicto_auditoria para documentar cuántos tests pasaron, cuántos fallaron y si el veredicto es APROBADO o RECHAZADO.

Usa una herramienta a la vez."""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("placeholder", "{agent_scratchpad}"),
    ("human", "{input}"),
])

tools = [leer_contexto_proyecto, guardar_tests, ejecutar_sandbox_docker, guardar_veredicto_auditoria]
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=10)

if __name__ == "__main__":
    print("="*50 + "\nAGENTE GUARDIAN INICIADO\n" + "="*50)
    resultado = executor.invoke({
        "input": "Ejecuta el flujo completo: lee el contexto, genera los tests Pytest para liquidar_nomina, ejecuta el sandbox y guarda el veredicto."
    })
    print("\n" + "="*50 + "\nSALIDA FINAL:\n" + resultado.get("output", "") + "\n" + "="*50)