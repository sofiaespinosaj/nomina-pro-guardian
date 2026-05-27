#!/usr/bin/env python3
"""
Agente Guardian — Motor de Nómina Pro (Universidad de Caldas)
LangChain + Qwen 2.5 Coder (Ollama) → genera Pytest → ejecuta en Sandbox.
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent

# ─── CONFIGURACIÓN DE RUTAS ───────────────────────────────────────────────────
MODEL        = "qwen2.5-coder:7b"
BASE_DIR     = Path(__file__).resolve().parent.parent
CASOS_FILE   = BASE_DIR / "casos_prueba.md"
ENGINE_FILE  = BASE_DIR / "src" / "engine.py"
TESTS_FILE   = BASE_DIR / "tests" / "test_generated.py"
SANDBOX_FILE = BASE_DIR / "guardian" / "sandbox.py"
VERDICT_FILE = BASE_DIR / "veredicto.json"

# Instanciamos a Qwen
llm = ChatOllama(model=MODEL, temperature=0)

# ─── TOOLS ────────────────────────────────────────────────────────────────────

@tool
def leer_contexto_proyecto() -> str:
    """Lee casos_prueba.md y src/engine.py para entender las reglas R1 a R5 y los 12 casos."""
    if not CASOS_FILE.exists() or not ENGINE_FILE.exists():
        return "ERROR: Faltan archivos base (casos_prueba.md o src/engine.py)."
    
    casos = CASOS_FILE.read_text(encoding="utf-8")
    codigo = ENGINE_FILE.read_text(encoding="utf-8")
    return f"--- ORÁCULO ---\n{casos}\n\n--- CÓDIGO FUENTE ---\n{codigo}"

@tool
def guardar_tests(codigo: str) -> str:
    """
    Escribe el codigo Python/Pytest en tests/test_generated.py.
    El parámetro 'codigo' DEBE ser estrictamente código Python puro y ejecutable.
    """
    codigo_limpio = codigo.replace("```python", "").replace("```", "").strip()

    # Tu validador defensivo: si Qwen se equivoca, la herramienta le responde con un error para que intente de nuevo
    if not _validar_codigo_tests(codigo_limpio):
        return (
            "ERROR INTERNO: El codigo generado está incompleto o tiene errores de sintaxis. "
            "Debes usar @pytest.mark.parametrize y asegurarte de incluir desde CP01 hasta CP12."
        )

    TESTS_FILE.parent.mkdir(exist_ok=True)
    TESTS_FILE.write_text(codigo_limpio, encoding="utf-8")
    return "test_generated.py guardado con éxito en la carpeta tests/."

def _validar_codigo_tests(codigo: str) -> bool:
    if not codigo: return False
    if "import pytest" not in codigo: return False
    if "from src.engine import liquidar_nomina" not in codigo: return False
    if "@pytest.mark.parametrize" not in codigo: return False
    return True

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

SYSTEM_PROMPT = """Eres el Agente Guardian de QA. Tu misión es ejecutar este flujo estrictamente en orden:

PASO 1 — Leer contexto
  Usa 'leer_contexto_proyecto' para obtener las reglas y los 12 casos de prueba.

PASO 2 — Generar código Pytest
  Usa 'guardar_tests' para escribir el código. 
  DEBES usar la lógica de diccionarios de Python. Extrae la entrada y la salida de los 12 casos del Oráculo y constrúyelos usando @pytest.mark.parametrize.
  Asegúrate de importar liquidar_nomina desde src.engine.

PASO 3 — Ejecutar Sandbox
  Usa 'ejecutar_sandbox_docker' para correr las pruebas. Si Docker te devuelve un error de importación o de código, VUELVE AL PASO 2 y corrige el código usando la herramienta guardar_tests.

PASO 4 — Guardar veredicto
  Una vez que Docker ejecute las pruebas (ya sea que pasen o fallen los asserts), usa 'guardar_veredicto_auditoria' con el resumen.

PASO 5 — FIN
  Detén la ejecución. NO reinicies el ciclo.

Usa una sola herramienta a la vez."""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("placeholder", "{agent_scratchpad}"),
    ("human", "{input}"),
])

tools = [leer_contexto_proyecto, guardar_tests, ejecutar_sandbox_docker, guardar_veredicto_auditoria]

# Qwen 2.5 Coder entiende Tool Calling nativo, así que usamos el orquestador puro
agent = create_tool_calling_agent(llm=llm, tools=tools, prompt=prompt)
executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    max_iterations=10,
    handle_parsing_errors=True
)

if __name__ == "__main__":
    print("="*50 + f"\nAGENTE GUARDIAN INICIADO ({MODEL})\n" + "="*50)
    resultado = executor.invoke({
        "input": "Ejecuta el flujo completo para automatizar y auditar el código."
    })
    print("\n" + "="*50 + "\nSALIDA FINAL:\n" + resultado.get("output", "") + "\n" + "="*50)