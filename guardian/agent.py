#!/usr/bin/env python3
"""
Agente Guardian — Motor de Nómina Pro (Universidad de Caldas)

Este módulo orquesta un agente de Inteligencia Artificial utilizando LangChain y el
modelo local Qwen 2.5 Coder vía Ollama. El agente es responsable de:
1. Leer los casos de prueba (Oráculo).
2. Generar el código automatizado de Pytest mediante una cadena dedicada.
3. Ejecutar las pruebas en un entorno Docker aislado (Sandbox).
4. Generar y almacenar un veredicto de auditoría estructurado.
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

# ─── 1. CONFIGURACIÓN DEL ENTORNO Y RUTAS ─────────────────────────────────────

MODEL = "qwen2.5-coder:7b"
BASE_DIR = Path(__file__).resolve().parent.parent

# Rutas de artefactos
CASOS_FILE = BASE_DIR / "casos_prueba.md"
TESTS_FILE = BASE_DIR / "tests" / "test_generated.py"
SANDBOX_FILE = BASE_DIR / "guardian" / "sandbox.py"
VERDICT_FILE = BASE_DIR / "veredicto.json"

# Inicialización del LLM con parámetros de memoria expandida para evitar cortes
llm = ChatOllama(
    model=MODEL, 
    temperature=0, 
    num_ctx=16384,      # Ampliación de la ventana de contexto para procesar el oráculo completo
    num_predict=8192    # Límite de tokens de salida para permitir la escritura de los 12 casos
)

# ─── 2. MOTOR DEDICADO DE GENERACIÓN DE CÓDIGO ────────────────────────────────

def _generar_codigo_pytest() -> str:
    """
    Cadena LLM independiente especializada únicamente en escribir el archivo Pytest.
    Utiliza un enfoque Few-Shot y directivas Anti-Attention Drift.
    """
    casos = CASOS_FILE.read_text(encoding="utf-8") if CASOS_FILE.exists() else ""

    peticion = f"""You are a meticulous QA Automation Engineer. Your task is to translate a Markdown Oracle into Pytest code.

CRITICAL DANGER - PREVENT ATTENTION DRIFT:
Previously, you made the mistake of MIXING data between test cases (e.g., using CP09's data in CP03).
To prevent this, you MUST process each '### CPXX' section as an ISOLATED ISLAND. DO NOT cross-contaminate data.

STRICT GENERATION RULES:
1. First line MUST be: import pytest
2. Second line MUST be: from src.engine import liquidar_nomina
3. Generate EXACTLY 12 test functions named test_cp01 through test_cp12, in order.
4. For EACH function, COPY the EXACT numbers and strings from the corresponding JSON. Do not change values.

MANDATORY STRUCTURE FOR ERROR CASES (e.g., CP02, CP07, CP08):
def test_cp02():
    entrada = {{"salario_base": ..., "horas_extras_diurnas": ..., "horas_extras_nocturnas": ..., "vlr_hora": ...}}
    with pytest.raises(ValueError) as exc_info:
        liquidar_nomina(**entrada)
    assert "exact string from mensaje_contiene" in str(exc_info.value)

MANDATORY STRUCTURE FOR NORMAL CASES:
def test_cp03():
    entrada = {{ ... exact copy of Input json ... }}
    esperado = {{ ... exact copy of Expected Output json ... }}
    assert liquidar_nomina(**entrada) == esperado

Here is the Oracle. Read carefully and DO NOT MIX THE DATA:
{casos}
"""
    respuesta = llm.invoke(peticion)
    texto = respuesta.content if hasattr(respuesta, "content") else str(respuesta)
    
    # Limpieza de las etiquetas Markdown del bloque de código
    texto = texto.replace("```python", "").replace("```", "").strip()
    return texto

def _validar_codigo(codigo: str) -> bool:
    """
    Validador heurístico para garantizar la integridad mínima del código generado 
    antes de enviarlo al Sandbox.
    """
    if not codigo or len(codigo) < 300:
        return False
    if "import pytest" not in codigo:
        return False
    if "from src.engine import liquidar_nomina" not in codigo:
        return False
    if codigo.count("def test_") < 10:
        return False
    if "assert True" in codigo:  # Prevención de asserts perezosos
        return False
    return True

# ─── 3. HERRAMIENTAS DEL AGENTE (TOOLS) ───────────────────────────────────────

@tool
def leer_contexto_proyecto(input_arg: str = "") -> str:
    """Lee casos_prueba.md y devuelve la confirmación de carga."""
    print("\n[1/4] Leyendo contexto del proyecto (Oráculo)...")
    if not CASOS_FILE.exists():
        return "ERROR: Falta el archivo base casos_prueba.md."
    
    casos = CASOS_FILE.read_text(encoding="utf-8")
    return f"Proyecto cargado. casos_prueba.md contiene {len(casos)} caracteres y los 12 escenarios."

@tool
def generar_y_guardar_tests(input_arg: str = "") -> str:
    """Genera test_generated.py con los 12 escenarios y lo guarda en tests/."""
    print("\n[2/4] Generando código Pytest vía cadena dedicada...")
    
    codigo = ""
    # Capa de resiliencia: 3 intentos en caso de alucinación del modelo
    for intento in range(1, 4):
        print(f"  Intento {intento}/3...")
        codigo = _generar_codigo_pytest()
        
        if _validar_codigo(codigo):
            print(f"  Validación estructural exitosa en intento {intento}.")
            break
            
        n_funciones = codigo.count("def test_")
        print(f"  Aviso: Código incompleto o malformado (encontradas {n_funciones} funciones). Reintentando...")

    if not _validar_codigo(codigo):
        return "ERROR: Falla crítica al generar código válido tras 3 intentos."

    TESTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    TESTS_FILE.write_text(codigo, encoding="utf-8")
    return f"SUCCESS: test_generated.py guardado con {codigo.count('def test_')} funciones de test."

@tool
def ejecutar_sandbox_docker(input_arg: str = "") -> str:
    """Lanza el entorno Docker de pruebas ejecutando sandbox.py."""
    print("\n[3/4] Ejecutando entorno Docker de pruebas aislado...")
    if not SANDBOX_FILE.exists() or not TESTS_FILE.exists():
        return "ERROR: Archivos necesarios para Docker no encontrados."
        
    resultado = subprocess.run(
        ["python", str(SANDBOX_FILE)],
        capture_output=True, text=True, cwd=str(BASE_DIR)
    )
    salida = resultado.stdout if resultado.stdout else resultado.stderr
    return salida if salida else "ERROR: El sandbox no produjo ninguna salida."

@tool
def guardar_veredicto_auditoria(resumen: str) -> str:
    """Guarda el veredicto final en veredicto.json en la raíz del proyecto."""
    print("\n[4/4] Analizando logs y guardando veredicto auditable...")
    
    # Intenta parsear el string a diccionario si el LLM lo envía como JSON string
    try:
        resumen_data = json.loads(resumen) if isinstance(resumen, str) else resumen
    except json.JSONDecodeError:
        resumen_data = resumen

    payload = {
        "timestamp": datetime.now().isoformat(),
        "modelo_ia": MODEL,
        "tests_generados": str(TESTS_FILE),
        "resumen_agente": resumen_data,
    }
    VERDICT_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return f"Veredicto auditable guardado en {VERDICT_FILE.name}"

# ─── 4. CEREBRO DEL AGENTE (PROMPT REACT) ─────────────────────────────────────

REACT_TEMPLATE = """You are Guardian Agent, a Senior QA Auditor. You must execute 4 steps in strict order using the available tools.

You have access to the following tools:
{tools}

MANDATORY FLOW (4 steps in order, ALL are mandatory):
Step 1: Use leer_contexto_proyecto to load the context.
Step 2: Use generar_y_guardar_tests to generate the Pytest script.
Step 3: You MUST use ejecutar_sandbox_docker to run the tests in the container. Do not skip this step unless Step 2 failed.
Step 4: Use guardar_veredicto_auditoria with a JSON string containing: total tests, passed, failed, bugs detected, and the verdict (APROBADO or RECHAZADO). 

CRITICAL: You MUST call 'guardar_veredicto_auditoria' BEFORE writing the Final Answer. 
If you do not call 'guardar_veredicto_auditoria', you fail your mission.


Use this EXACT format for each step:

Thought: [your reasoning]
Action: [exact name of the tool from this list: {tool_names}]
Action Input: [the input for the tool, or the word "none"]
Observation: [tool's result]

Once you have called guardar_veredicto_auditoria and received its Observation, write:

Thought: I must call guardar_veredicto_auditoria before writing Final Answer.
Action: guardar_veredicto_auditoria
Action Input: [JSON string with total, passed, failed, bugs_detectados, veredicto]
Observation: [tool result]
Thought: I have completed all steps including Docker execution and saving the verdict.
Final Answer: [A clean summary of the audit]
Begin now.

Question: {input}
{agent_scratchpad}"""

prompt = PromptTemplate.from_template(REACT_TEMPLATE)

tools = [
    leer_contexto_proyecto,
    generar_y_guardar_tests,
    ejecutar_sandbox_docker,
    guardar_veredicto_auditoria,
]

agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=15,
    handle_parsing_errors=True,
)

# ─── 5. PUNTO DE ENTRADA PRINCIPAL ────────────────────────────────────────────

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
                "Execute the audit flow in 4 strict steps: "
                "1) leer_contexto_proyecto, "
                "2) generar_y_guardar_tests, "
                "3) ejecutar_sandbox_docker (Mandatory), "
                "4) guardar_veredicto_auditoria."
            )
        })

        print(f"\n{sep}")
        print("VEREDICTO DEL AGENTE GUARDIAN:")
        print(sep)
        print(resultado.get("output", "(sin respuesta)").strip())
        print(sep)

        if VERDICT_FILE.exists():
            print(f"\nArchivo de auditoría generado: {VERDICT_FILE.name}")

    except KeyboardInterrupt:
        print("\nEjecución interrumpida por el usuario.")
        sys.exit(0)
    except Exception as exc:
        print(f"\nERROR CRÍTICO en el Agente Guardian: {exc}", file=sys.stderr)
        sys.exit(1)