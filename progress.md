# Estado del Progreso - Célula Nómina Pro

## Tareas Completadas
- [x] **TASK-LD-01**: Crear carpetas (`src/`, `docs/`, `guardian/`) y `README.md` maestro.
- [x] **TASK-LD-02**: Escribir el cascarón de la función `liquidar_nomina` en `src/engine.py` con type hints, docstring R1-R5 y `NotImplementedError`.

## Tareas Pendientes
- [ ] **TASK-LD-03**: Programar las validaciones de errores (R5: salario_base < $1.300.000, horas negativas, vlr_hora <= 0). **(SIGUIENTE PASO)**
- [ ] **TASK-LD-04**: Programar las fórmulas matemáticas de la nómina (R1-R4).
- [ ] **TASK-CEL-01**: Diseñar el Oráculo `docs/casos_prueba.md` con los 10 escenarios críticos.
- [ ] **TASK-AI-01**: Implementar `guardian/agent.py` (Agente LangChain).
- [ ] **TASK-QA-01**: Implementar `guardian/sandbox.py` (Orquestador Docker).
- [ ] **TASK-QA-02**: Crear `Dockerfile` con imagen base `guardian-sandbox`.
