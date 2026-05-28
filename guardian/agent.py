#!/usr/bin/env python3
"""
Agente Guardian — Motor de Nómina Pro (Universidad de Caldas)
LangChain + qwen2.5-coder:7b (Ollama) con ReAct → genera Pytest → ejecuta en Sandbox.
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
MODEL    = "qwen2.5-coder:7b"
BASE_DIR = Path(__file__).resolve().parent.parent
CASOS_FILE   = BASE_DIR / "casos_prueba.md"
ENGINE_FILE  = BASE_DIR / "src" / "engine.py"
TESTS_FILE   = BASE_DIR / "tests" / "test_generated.py"
SANDBOX_FILE = BASE_DIR / "guardian" / "sandbox.py"
VERDICT_FILE = BASE_DIR / "veredicto.json"

llm = ChatOllama(model=MODEL, temperature=0)

# ─── GENERADOR DEDICADO DE PYTEST ─────────────────────────────────────────────
def _generar_codigo_pytest() -> str:
    casos = CASOS_FILE.read_text(encoding="utf-8") if CASOS_FILE.exists() else ""

    peticion = f"""You are a Python testing expert. Write a pytest file that tests the function liquidar_nomina from src.engine.

The file MUST start with exactly these two lines:
import pytest
from src.engine import liquidar_nomina



Then write one test function per scenario below. Use this pattern for normal cases:
def test_cp01():
    r = liquidar_nomina(salario_base, horas_extras_diurnas, horas_extras_nocturnas, vlr_hora)
    assert r["key"] == pytest.approx(expected, abs=0.1)

Use this pattern for error cases:
def test_cp02():
    with pytest.raises(ValueError):
        liquidar_nomina(salario_base, horas_extras_diurnas, horas_extras_nocturnas, vlr_hora)

Here are the test scenarios with exact input and expected output values:
{casos}

Output ONLY the Python code. No markdown. No explanations. Start typing the code now.
"""
    respuesta = llm.invoke(peticion)
    texto = respuesta.content if hasattr(respuesta, "content") else str(respuesta)

    print(f"\n  >>>DEBUG<<<\n{repr(texto[:400])}\n  >>>FIN<<<\n")

    texto = texto.replace("```python", "").replace("```", "").strip()
    return texto

# ─── VALIDADOR ────────────────────────────────────────────────────────────────
def _validar_codigo(codigo: str) -> bool:
    if not codigo or len(codigo) < 300:
        return False
    if "import pytest" not in codigo:
        return False
    if "from src.engine import liquidar_nomina" not in codigo:
        return False
    if codigo.count("def test_") < 10:
        return False
    if "assert True" in codigo:
        return False
    return True


# ─── TOOLS ────────────────────────────────────────────────────────────────────

@tool
def leer_contexto_proyecto(input: str = "") -> str:
    """Lee casos_prueba.md y src/engine.py y devuelve un resumen del proyecto. No requiere argumentos."""
    print("\n[1/4] Leyendo contexto del proyecto...")
    if not CASOS_FILE.exists() or not ENGINE_FILE.exists():
        return "ERROR: Faltan archivos base (casos_prueba.md o src/engine.py)."
    casos  = CASOS_FILE.read_text(encoding="utf-8")
    codigo = ENGINE_FILE.read_text(encoding="utf-8")
    return (
        f"Proyecto cargado correctamente. "
        f"casos_prueba.md tiene {len(casos)} caracteres con escenarios CP01..CP12. "
        f"engine.py tiene {len(codigo)} caracteres con liquidar_nomina R1-R5. "
        f"Contexto listo para generar los escenarios de validacion academica."
    )


@tool
def generar_y_guardar_tests(input: str = "") -> str:
    """Genera test_generated.py con los 12 escenarios de validacion academica CP01-CP12 y lo guarda en tests/. No requiere argumentos."""
    print("\n[2/4] Generando codigo Pytest via cadena dedicada...")
    codigo = ""
    for intento in range(1, 4):
        print(f"  Intento {intento}/3...")
        codigo = _generar_codigo_pytest()
        if _validar_codigo(codigo):
            print(f"  Validacion exitosa en intento {intento}.")
            break
        n = codigo.count("def test_")
        motivos = []
        if len(codigo) < 300: motivos.append(f"muy corto ({len(codigo)} chars)")
        if "import pytest" not in codigo: motivos.append("falta import pytest")
        if "from src.engine import liquidar_nomina" not in codigo: motivos.append("falta import liquidar_nomina")
        if n < 10: motivos.append(f"solo {n} funciones (minimo 10)")
        print(f"  Fallido: {', '.join(motivos)}")

    if not _validar_codigo(codigo):
        return "ERROR: No se pudo generar codigo valido tras 3 intentos. Verifica que qwen2.5-coder:7b este instalado."

    TESTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    TESTS_FILE.write_text(codigo, encoding="utf-8")
    return f"SUCCESS: test_generated.py guardado con {codigo.count('def test_')} funciones de test."


@tool
def ejecutar_sandbox_docker(input: str = "") -> str:
    """Lanza el entorno Docker de pruebas aislado ejecutando sandbox.py. Solo llamar si generar_y_guardar_tests respondio SUCCESS. No requiere argumentos."""
    print("\n[3/4] Ejecutando entorno Docker de pruebas aislado...")
    if not SANDBOX_FILE.exists():
        return "ERROR: sandbox.py no existe."
    if not TESTS_FILE.exists():
        return "ERROR: test_generated.py no existe. Ejecuta generar_y_guardar_tests primero."
    if not TESTS_FILE.read_text(encoding="utf-8").strip():
        return "ERROR: test_generated.py esta vacio."
    resultado = subprocess.run(
        ["python", str(SANDBOX_FILE)],
        capture_output=True, text=True, cwd=str(BASE_DIR),
    )
    salida = resultado.stdout if resultado.stdout else resultado.stderr
    return salida if salida else "ERROR: El sandbox no produjo ninguna salida."


@tool
def guardar_veredicto_auditoria(resumen: str) -> str:
    """Guarda el veredicto final en veredicto.json. El argumento es un string con: total, aprobadas, reprobadas, bugs y veredicto APROBADO o RECHAZADO."""
    print("\n[4/4] Guardando veredicto auditable...")
    if isinstance(resumen, dict):
        resumen = json.dumps(resumen, ensure_ascii=False)
    payload = {
        "timestamp": datetime.now().isoformat(),
        "modelo_ia": MODEL,
        "tests_generados": str(TESTS_FILE),
        "resumen_agente": resumen,
    }
    VERDICT_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return f"Veredicto auditable guardado en {VERDICT_FILE.name}"


# ─── PROMPT REACT ─────────────────────────────────────────────────────────────

REACT_TEMPLATE = """Eres Agente Guardian, un auditor senior de QA. Debes ejecutar 4 pasos en orden estricto usando las herramientas disponibles.

Tienes acceso a estas herramientas:
{tools}

FLUJO OBLIGATORIO (4 pasos en orden, TODOS son obligatorios):
Paso 1: Usa leer_contexto_proyecto para cargar el contexto.
Paso 2: Usa generar_y_guardar_tests para generar los escenarios de validacion academica.
Paso 3: SOLO si paso 2 respondio SUCCESS, usa ejecutar_sandbox_docker.
Paso 4: OBLIGATORIO SIEMPRE. Usa guardar_veredicto_auditoria con un string que contenga: total de pruebas, cuantas pasaron, cuantas fallaron, bugs detectados y veredicto APROBADO o RECHAZADO. DEBES llamar a esta herramienta antes de escribir Final Answer.

REGLA CRITICA: No puedes escribir Final Answer sin haber llamado primero a guardar_veredicto_auditoria.

Usa este formato EXACTO en cada paso:

Thought: [tu razonamiento]
Action: [nombre exacto de la herramienta de esta lista: {tool_names}]
Action Input: [el input para la herramienta, o la palabra none si no requiere argumentos]
Observation: [resultado de la herramienta]

Cuando hayas llamado guardar_veredicto_auditoria y obtenido su Observation, entonces escribe:
Thought: He completado todos los pasos incluyendo guardar el veredicto.
Final Answer: [resumen con total, aprobadas, reprobadas, bugs y veredicto]

Comienza ahora.

Question: {input}
{agent_scratchpad}"""

prompt = PromptTemplate.from_template(REACT_TEMPLATE)

tools = [
    leer_contexto_proyecto,
    generar_y_guardar_tests,
    ejecutar_sandbox_docker,
    guardar_veredicto_auditoria,
]

agent    = create_react_agent(llm=llm, tools=tools, prompt=prompt)
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=20,
    handle_parsing_errors=True,
)

# ─── PUNTO DE ENTRADA ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    sep = "=" * 65
    print(sep)
    print("  AGENTE GUARDIAN — UNIVERSIDAD DE CALDAS")
    print(f"  Modelo : {MODEL} via Ollama")
    print(f"  Fecha  : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(sep)

    try:
        resultado = executor.invoke({
            "input": (
                "Ejecuta el flujo de auditoria en 4 pasos en orden: "
                "1) leer_contexto_proyecto, "
                "2) generar_y_guardar_tests, "
                "3) ejecutar_sandbox_docker solo si paso 2 fue SUCCESS, "
                "4) guardar_veredicto_auditoria con string del resumen."
            )
        })

        print(f"\n{sep}")
        print("VEREDICTO DEL AGENTE GUARDIAN:")
        print(sep)
        print(resultado.get("output", "(sin respuesta)").strip())
        print(sep)

        if VERDICT_FILE.exists():
            print(f"\nArchivo de auditoria generado: {VERDICT_FILE.name}")

    except KeyboardInterrupt:
        print("\nEjecucion interrumpida por el usuario.")
        sys.exit(0)
    except Exception as exc:
        print(f"\nERROR en el Agente Guardian: {exc}", file=sys.stderr)
        sys.exit(1)