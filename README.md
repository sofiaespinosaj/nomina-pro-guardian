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

```text
├── casos_prueba.md             # [CÉLULA] Oráculo con los 10 escenarios críticos
├── src/
│   └── engine.py               # [LEAD DEV] Motor de nómina con liquidar_nomina
├── guardian/                   # [PENDIENTE] Agente LangChain y sandbox Docker
├── progress.md                 # Seguimiento de avance
├── .gitignore                  # Archivos ignorados por git
└── README.md                   # Este archivo
```

---

## ✅ Estado Actual

| Artefacto | Estado | US |
|---|---|---|
| `src/engine.py` | Completado | US-NOM01 |
| `casos_prueba.md` | Completado | US-NOM02 |
| `guardian/agent.py` | Pendiente | - |
| `guardian/sandbox.py` | Pendiente | - |
| `Dockerfile` | Pendiente | - |

---

## 📋 El Contrato del Motor (`src/engine.py`)

```python
def liquidar_nomina(
    salario_base: float,
    horas_extras_diurnas: int,
    horas_extras_nocturnas: int,
    vlr_hora: float
) -> dict:
```

### Reglas de Negocio (R1 - R5)

| Regla | Descripción |
|---|---|
| **R1** | Horas extras diurnas con recargo del 25% sobre vlr_hora |
| **R2** | Horas extras nocturnas con recargo del 75% sobre vlr_hora |
| **R3** | Descuento de 4% salud + 4% pensión sobre total devengado |
| **R4** | Auxilio de transporte $162.000 si salario_base ≤ $2.600.000 |
| **R5** | Validación: salario < $1.300.000 o horas negativas lanza `ValueError` |

### Diccionario de Salida

| Llave | Descripción |
|---|---|
| `salario_base` | Salario base mensual |
| `total_extras_diurnas` | vlr_hora × horas_extras_diurnas × 1.25 |
| `total_extras_nocturnas` | vlr_hora × horas_extras_nocturnas × 1.75 |
| `total_devengado` | salario_base + total_extras_diurnas + total_extras_nocturnas |
| `descuento_salud` | 4% de total_devengado |
| `descuento_pension` | 4% de total_devengado |
| `auxilio_transporte` | $162.000 si salario_base ≤ $2.600.000, sino $0 |
| `neto_pagar` | total_devengado - descuento_salud - descuento_pension + auxilio_transporte |

---

## 🔄 Flujo de Ejecución del Guardian (Próximamente)

```bash
python guardian/agent.py src/engine.py
```

1. **Análisis:** El agente lee `src/engine.py` y `casos_prueba.md`.
2. **Generación:** Escribe de forma autónoma el archivo `test_generated.py`.
3. **Sandbox:** Invoca a Docker ejecutando `pytest --json-report` de manera aislada.
4. **Reporte:** Consume el JSON y genera un reporte Markdown con veredicto **APROBADO** o **RECHAZADO**.
