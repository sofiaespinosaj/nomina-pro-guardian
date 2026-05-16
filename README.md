# The Quality Guardian MVP - Nómina Pro 🚀
### COIL · Software III (U. de Caldas × U. Manuela Beltrán)

Este repositorio contiene el sistema agéntico de segunda generación (2G) **The Quality Guardian**. El objetivo del sistema es auditar de forma autónoma, aislada y local un motor de cálculo de nómina colombiana, emitiendo un veredicto técnico basado en un oráculo de especificaciones.

---

## 🛠️ Stack Tecnológico (100% Open Source)
- **Cerebro / LLM:** Llama 3 (8B) operando localmente vía `Ollama`.
- **Orquestación:** `LangChain` (Python).
- **Lenguaje Core:** `Python 3.11+` (Strict Typing).
- **Entorno de Pruebas:** `Pytest` + `pytest-json-report`.
- **Sandbox de Aislamiento:** `Docker`.

---

## 📂 Estructura del Proyecto
Cualquier modificación o adición de código debe respetar estrictamente esta topología:

```text
├── docs/
│   └── casos_prueba.md       # [CÉLULA] Oráculo con los 10 escenarios críticos (Fase 0)
├── src/
│   └── engine.py             # [LEAD DEV] Motor de nómina con la función liquidar_nomina
├── guardian/
│   ├── agent.py              # [AI ENG] Agente LangChain que genera test_generated.py
│   └── sandbox.py            # [QA/DEVOPS] Orquestador de Docker y extractor de .report.json
├── test_generated.py         # [AGENTE] Archivo de pruebas autogenerado (Efímero)
├── Dockerfile                # [QA/DEVOPS] Imagen base 'guardian-sandbox' con Pytest
└── README.md                 # Este archivo: Contrato Técnico Maestro
```
## 📋 El Contrato del Motor (src/engine.py)
La función principal implementada por el Lead Developer debe cumplir rigurosamente con la siguiente firma y tipos de datos:

```python
def liquidar_nomina(
    salario_base: float,
    horas_extras_diurnas: int,
    horas_extras_nocturnas: int,
    vlr_hora: float
) -> dict:
    """
    Liquida la nómina según las reglas de negocio colombianas (R1 - R5).
    Retorna un diccionario con las propiedades financieras redondeadas a 2 decimales.
    """
    pass
```

### Estructura Mandatoria del Diccionario de Salida
Cualquier respuesta exitosa del motor debe retornar estas llaves exactas:

- `"salario_base"`: float
- `"total_extras_diurnas"`: float (Recargo del 25% sobre vlr_hora)
- `"total_extras_nocturnas"`: float (Recargo del 75% sobre vlr_hora)
- `"total_devengado"`: float (salario_base + total_extras_diurnas + total_extras_nocturnas)
- `"descuento_salud"`: float (4% sobre total_devengado)
- `"descuento_pension"`: float (4% sobre total_devengado)
- `"auxilio_transporte"`: float (162000.0 si salario_base <= 2600000, de lo contrario 0.0)
- `"neto_pagar"`: float (total_devengado - descuento_salud - descuento_pension + auxilio_transporte)

---

## 🔄 Flujo de Ejecución del Guardian
El sistema operará bajo una sola línea de comando como punto de entrada:

```bash
python guardian/agent.py src/engine.py
```

1. **Análisis:** El agente lee `src/engine.py` y `docs/casos_prueba.md`.
2. **Generación:** Escribe de forma autónoma el archivo `test_generated.py`.
3. **Sandbox:** Invoca a Docker ejecutando `pytest --json-report` de manera aislada.
4. **Reporte:** Consume el JSON y genera un reporte Markdown con veredicto **APROBADO** o **RECHAZADO**.
