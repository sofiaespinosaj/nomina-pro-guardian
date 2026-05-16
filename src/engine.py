def liquidar_nomina(
    salario_base: float,
    horas_extras_diurnas: int,
    horas_extras_nocturnas: int,
    vlr_hora: float
) -> dict:
    """
    Liquida la nómina mensual de un empleado aplicando la legislación colombiana vigente 
    y las reglas de negocio estipuladas para el proyecto Nómina Pro (R1 - R5).

    Reglas de Negocio a evaluar por el Quality Guardian:
    - R1 (Recargo Diurno): 25% sobre el valor de la hora ordinaria (vlr_hora * 1.25).
    - R2 (Recargo Nocturno): 75% sobre el valor de la hora ordinaria (vlr_hora * 1.75).
    - R3 (Seguridad Social): Deducción de 4% para Salud y 4% para Pensión calculados 
      exclusivamente sobre el Total Devengado (Salario Base + Extras). El Auxilio de 
      Transporte no hace parte de esta base de cotización.
    - R4 (Auxilio de Transporte): Se adiciona un valor fijo de $162.000 únicamente si el 
      salario_base es menor o igual a $2.600.000.
    - R5 (Validación Defensiva): Se debe lanzar una excepción ValueError con un mensaje 
      claro si salario_base < $1.300.000 o si alguna cantidad de horas extras es negativa, 
      o si vlr_hora <= 0.

    Parámetros:
    -----------
    salario_base : float
        Asignación salarial mensual fija del trabajador (Mínimo legal simulado: $1.300.000).
    horas_extras_diurnas : int
        Cantidad de horas extras laboradas en jornada diurna (Debe ser >= 0).
    horas_extras_nocturnas : int
        Cantidad de horas extras laboradas en jornada nocturna (Debe ser >= 0).
    vlr_hora : float
        Valor de la hora ordinaria de trabajo calculada para el empleado (Debe ser > 0).

    Retorna:
    --------
    dict
        Diccionario con la liquidación detallada. Todas las propiedades numéricas de salida 
        deben estar redondeadas estrictamente a dos (2) decimales. El formato exacto es:
        {
            "salario_base": float,
            "total_extras_diurnas": float,
            "total_extras_nocturnas": float,
            "total_devengado": float,
            "descuento_salud": float,
            "descuento_pension": float,
            "auxilio_transporte": float,
            "neto_pagar": float
        }

    Excepciones:
    ------------
    ValueError
        Si los datos de entrada violan las restricciones de seguridad descritas en R5.
    """

    # --- CAPA DEFENSIVA DE VALIDACIÓN (Regla R5) ---
    if salario_base < 1300000.0:
        raise ValueError(f"Error de validación (R5): El salario base ({salario_base}) no puede ser inferior al mínimo legal de $1.300.000.")
        
    if horas_extras_diurnas < 0:
        raise ValueError(f"Error de validación (R5): La cantidad de horas extras diurnas ({horas_extras_diurnas}) no puede ser negativa.")
        
    if horas_extras_nocturnas < 0:
        raise ValueError(f"Error de validación (R5): La cantidad de horas extras nocturnas ({horas_extras_nocturnas}) no puede ser negativa.")
        
    if vlr_hora <= 0:
        raise ValueError(f"Error de validación (R5): El valor de la hora ordinaria ({vlr_hora}) debe ser estrictamente mayor a cero.")

    # --- NÚCLEO MATEMÁTICO DE LIQUIDACIÓN (Reglas R1 - R4) ---
    total_extras_diurnas = horas_extras_diurnas * vlr_hora * 1.25
    total_extras_nocturnas = horas_extras_nocturnas * vlr_hora * 1.75
    
    total_devengado = salario_base + total_extras_diurnas + total_extras_nocturnas
    
    descuento_salud = total_devengado * 0.04
    descuento_pension = total_devengado * 0.04
    
    auxilio_transporte = 162000.0 if salario_base <= 2600000.0 else 0.0
    
    neto_pagar = total_devengado - descuento_salud - descuento_pension + auxilio_transporte

    # --- RETORNO ESTRUCTURADO Y REDONDEADO A 2 DECIMALES ---
    return {
        "salario_base": round(salario_base, 2),
        "total_extras_diurnas": round(total_extras_diurnas, 2),
        "total_extras_nocturnas": round(total_extras_nocturnas, 2),
        "total_devengado": round(total_devengado, 2),
        "descuento_salud": round(descuento_salud, 2),
        "descuento_pension": round(descuento_pension, 2),
        "auxilio_transporte": round(auxilio_transporte, 2),
        "neto_pagar": round(neto_pagar, 2)
    }
