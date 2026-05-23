# Oráculo de Pruebas Automatizadas - US-NOM02 (Versión Corregida)

Este documento contiene la matriz oficial de escenarios de prueba adaptada rigurosamente al contrato inmutable de `src/engine.py`.

## Matriz de Escenarios de Prueba

### CP01: Validación de Caso Límite Inclusivo para Auxilio de Transporte (R4)
* **Regla de Negocio:** R4 - Umbral del Auxilio de Transporte (Límite Exacto Inclusivo)
* **Descripción:** Al estar exactamente en la frontera de $2.600.000, el empleado sigue siendo beneficiario del auxilio de transporte según la regla ("menor o igual").
* **Entrada (Input):**
    ```json
    {
      "salario_base": 2600000.0,
      "horas_extras_diurnas": 0,
      "horas_extras_nocturnas": 0,
      "vlr_hora": 10833.33
    }
    ```
* **Salida Esperada (Expected Output):**
    ```json
    {
      "salario_base": 2600000.0,
      "total_extras_diurnas": 0.0,
      "total_extras_nocturnas": 0.0,
      "total_devengado": 2600000.0,
      "descuento_salud": 104000.0,
      "descuento_pension": 104000.0,
      "auxilio_transporte": 162000.0,
      "neto_pagar": 2554000.0
    }
    ```

### CP02: Validación de Control de Horas Negativas (R5)
* **Regla de Negocio:** R5 - Validaciones de Consistencia (Excepción)
* **Descripción:** El sistema debe abortar y lanzar un ValueError si se ingresan horas negativas.
* **Entrada (Input):**
    ```json
    {
      "salario_base": 1500000.0,
      "horas_extras_diurnas": -5,
      "horas_extras_nocturnas": 0,
      "vlr_hora": 6250.0
    }
    ```
* **Salida Esperada (Expected Output):**
    ```json
    {
      "error_esperado": "ValueError",
      "mensaje_contiene": "no puede ser negativa"
    }
    ```

### CP03: Verificación Exacta de Descuento de Salud del 4% (R3)
* **Regla de Negocio:** R3 - Regla de Seguridad Social
* **Descripción:** Comprobar que el descuento de salud sea el 4% exacto del total devengado.
* **Entrada (Input):**
    ```json
    {
      "salario_base": 2000000.0,
      "horas_extras_diurnas": 0,
      "horas_extras_nocturnas": 0,
      "vlr_hora": 8333.33
    }
    ```
* **Salida Esperada (Expected Output):**
    ```json
    {
      "total_devengado": 2000000.0,
      "descuento_salud": 80000.0,
      "descuento_pension": 80000.0
    }
    ```

### CP04: Registro de Horas Extras Mixtas (R1, R2, R3 - Caso de la Célula)
* **Regla de Negocio:** R1 y R2 - Horas Extras Mixtas Simultáneas
* **Descripción:** Liquidación simultánea de 4 extras diurnas (+25%) y 2 nocturnas (+75%) con salario base de $1.300.000 y valor hora de $5.416.67.
* **Entrada (Input):**
    ```json
    {
      "salario_base": 1300000.0,
      "horas_extras_diurnas": 4,
      "horas_extras_nocturnas": 2,
      "vlr_hora": 5416.67
    }
    ```
* **Salida Esperada (Expected Output):**
    ```json
    {
      "total_extras_diurnas": 27083.35,
      "total_extras_nocturnas": 18958.35,
      "total_devengado": 1346041.70
    }
    ```

### CP05: Exclusión de Auxilio de Transporte por Alto Salario (R4)
* **Regla de Negocio:** R4 - Exclusión de subsidio por superar los 2 SMMLV.
* **Entrada (Input):**
    ```json
    {
      "salario_base": 3000000.0,
      "horas_extras_diurnas": 0,
      "horas_extras_nocturnas": 0,
      "vlr_hora": 12500.0
    }
    ```
* **Salida Esperada (Expected Output):**
    ```json
    {
      "auxilio_transporte": 0.0,
      "neto_pagar": 2760000.0
    }
    ```

### CP06: Empleado con Salario Mínimo y sin Extras (R4)
* **Regla de Negocio:** R4 - Caso base con derecho a auxilio de transporte completo.
* **Entrada (Input):**
    ```json
    {
      "salario_base": 1300000.0,
      "horas_extras_diurnas": 0,
      "horas_extras_nocturnas": 0,
      "vlr_hora": 5416.67
    }
    ```
* **Salida Esperada (Expected Output):**
    ```json
    {
      "total_devengado": 1300000.0,
      "auxilio_transporte": 162000.0,
      "neto_pagar": 1358000.0
    }
    ```

### CP07: Validación de Excepción por Salario Inferior al Mínimo (R5)
* **Regla de Negocio:** R5 - Control de salario ilegal.
* **Entrada (Input):**
    ```json
    {
      "salario_base": 1200000.0,
      "horas_extras_diurnas": 0,
      "horas_extras_nocturnas": 0,
      "vlr_hora": 5000.0
    }
    ```
* **Salida Esperada (Expected Output):**
    ```json
    {
      "error_esperado": "ValueError",
      "mensaje_contiene": "inferior al mínimo legal"
    }
    ```

### CP08: Excepción por Valor de Hora Cero o Negativo (R5 - Caso de la Célula)
* **Regla de Negocio:** R5 - Segundo escenario de control de consistencia de la célula.
* **Entrada (Input):**
    ```json
    {
      "salario_base": 1600000.0,
      "horas_extras_diurnas": 10,
      "horas_extras_nocturnas": 0,
      "vlr_hora": 0.0
    }
    ```
* **Salida Esperada (Expected Output):**
    ```json
    {
      "error_esperado": "ValueError",
      "mensaje_contiene": "debe ser estrictamente mayor a cero"
    }
    ```

### CP09: Deducción de Pensión Obligatoria del 4% (R3)
* **Regla de Negocio:** R3 - Descuento de pensión aislado.
* **Entrada (Input):**
    ```json
    {
      "salario_base": 2500000.0,
      "horas_extras_diurnas": 0,
      "horas_extras_nocturnas": 0,
      "vlr_hora": 10416.67
    }
    ```
* **Salida Esperada (Expected Output):**
    ```json
    {
      "total_devengado": 2500000.0,
      "descuento_pension": 100000.0
    }
    ```

### CP10: Liquidación Integral Completa con Reglas Cruzadas (R1, R2, R3, R4)
* **Regla de Negocio:** Integración Matemática Total
* **Entrada (Input):**
    ```json
    {
      "salario_base": 1300000.0,
      "horas_extras_diurnas": 4,
      "horas_extras_nocturnas": 2,
      "vlr_hora": 5416.67
    }
    ```
* **Salida Esperada (Expected Output):**
    ```json
    {
      "salario_base": 1300000.0,
      "total_extras_diurnas": 27083.35,
      "total_extras_nocturnas": 18958.35,
      "total_devengado": 1346041.70,
      "descuento_salud": 53841.67,
      "descuento_pension": 53841.67,
      "auxilio_transporte": 162000.0,
      "neto_pagar": 1400358.36
    }
    ```

### CP11: Escenario de Estrés Mixto Máximo con Salario Alto y Centavos (Caso Propio de la Célula)
* **Regla de Negocio:** R1, R2, R3 y R4 - Integración de Horas Mixtas Simultáneas con Exclusión de Auxilio de Transporte.
* **Descripción:** Diseñado por la célula para estresar el algoritmo con un salario base alto ($2.800.000) que supera el umbral de auxilio de transporte, combinando una cantidad alta de horas extras diurnas (12) y nocturnas (8) con un valor de hora con decimales complejos ($11.666,67).
* **Entrada (Input):**
    ```json
    {
      "salario_base": 2800000.0,
      "horas_extras_diurnas": 12,
      "horas_extras_nocturnas": 8,
      "vlr_hora": 11666.67
    }
    ```
* **Salida Esperada (Expected Output):**
    ```json
    {
      "salario_base": 2800000.0,
      "total_extras_diurnas": 175000.05,
      "total_extras_nocturnas": 163333.38,
      "total_devengado": 3138333.43,
      "descuento_salud": 125533.34,
      "descuento_pension": 125533.34,
      "auxilio_transporte": 0.0,
      "neto_pagar": 2887266.76
    }
    ```

### CP12: Escenario Límite de Frontera Mínima con Horas Extras (Caso Propio de la Célula)
* **Regla de Negocio:** R1, R3, R4 y R5 - Frontera del Salario Mínimo Legal con Trabajo Suplementario.
* **Descripción:** Validar que un empleado en el límite inferior estricto de salario ($1.300.000) pueda acumular horas extras diurnas sin alterar su derecho al auxilio de transporte ni violar la capa defensiva R5.
* **Entrada (Input):**
    ```json
    {
      "salario_base": 1300000.0,
      "horas_extras_diurnas": 5,
      "horas_extras_nocturnas": 0,
      "vlr_hora": 5416.67
    }
    ```
* **Salida Esperada (Expected Output):**
    ```json
    {
      "salario_base": 1300000.0,
      "total_extras_diurnas": 33854.19,
      "total_extras_nocturnas": 0.0,
      "total_devengado": 1333854.19,
      "descuento_salud": 53354.17,
      "descuento_pension": 53354.17,
      "auxilio_transporte": 162000.0,
      "neto_pagar": 1389145.85
    }
    ```
