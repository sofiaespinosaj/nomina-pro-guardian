import pytest
from src.engine import liquidar_nomina

casos = [
    ("CP01",
     {"salario_base": 2600000.0, "horas_extras_diurnas": 0, "horas_extras_nocturnas": 0, "vlr_hora": 10833.33},
     {"salario_base": 2600000.0, "total_extras_diurnas": 0.0, "total_extras_nocturnas": 0.0, "total_devengado": 2600000.0, "descuento_salud": 104000.0, "descuento_pension": 104000.0, "auxilio_transporte": 162000.0, "neto_pagar": 2554000.0}),
    ("CP02",
     {"salario_base": 1500000.0, "horas_extras_diurnas": -5, "horas_extras_nocturnas": 0, "vlr_hora": 6250.0},
     {"error_esperado": "ValueError"}),
    ("CP03",
     {"salario_base": 2000000.0, "horas_extras_diurnas": 0, "horas_extras_nocturnas": 0, "vlr_hora": 8333.33},
     {"total_devengado": 2000000.0, "descuento_salud": 80000.0, "descuento_pension": 80000.0}),
    ("CP04",
     {"salario_base": 1300000.0, "horas_extras_diurnas": 4, "horas_extras_nocturnas": 2, "vlr_hora": 5416.67},
     {"total_extras_diurnas": 27083.35, "total_extras_nocturnas": 18958.35, "total_devengado": 1346041.70}),
    ("CP05",
     {"salario_base": 3000000.0, "horas_extras_diurnas": 0, "horas_extras_nocturnas": 0, "vlr_hora": 12500.0},
     {"auxilio_transporte": 0.0, "neto_pagar": 2760000.0}),
    ("CP06",
     {"salario_base": 1300000.0, "horas_extras_diurnas": 0, "horas_extras_nocturnas": 0, "vlr_hora": 5416.67},
     {"total_devengado": 1300000.0, "auxilio_transporte": 162000.0, "neto_pagar": 1358000.0}),
    ("CP07",
     {"salario_base": 1200000.0, "horas_extras_diurnas": 0, "horas_extras_nocturnas": 0, "vlr_hora": 5000.0},
     {"error_esperado": "ValueError"}),
    ("CP08",
     {"salario_base": 1600000.0, "horas_extras_diurnas": 10, "horas_extras_nocturnas": 0, "vlr_hora": 0.0},
     {"error_esperado": "ValueError"}),
    ("CP09",
     {"salario_base": 2500000.0, "horas_extras_diurnas": 0, "horas_extras_nocturnas": 0, "vlr_hora": 10416.67},
     {"total_devengado": 2500000.0, "descuento_pension": 100000.0}),
    ("CP10",
     {"salario_base": 1300000.0, "horas_extras_diurnas": 4, "horas_extras_nocturnas": 2, "vlr_hora": 5416.67},
     {"total_extras_diurnas": 27083.35, "total_extras_nocturnas": 18958.35, "total_devengado": 1346041.70, "descuento_salud": 53841.67, "descuento_pension": 53841.67, "auxilio_transporte": 162000.0, "neto_pagar": 1400358.36}),
    ("CP11",
     {"salario_base": 2800000.0, "horas_extras_diurnas": 12, "horas_extras_nocturnas": 8, "vlr_hora": 11666.67},
     {"total_extras_diurnas": 175000.05, "total_extras_nocturnas": 163333.38, "total_devengado": 3138333.43, "descuento_salud": 125533.34, "descuento_pension": 125533.34, "auxilio_transporte": 0.0, "neto_pagar": 2887266.76}),
    ("CP12",
     {"salario_base": 1300000.0, "horas_extras_diurnas": 5, "horas_extras_nocturnas": 0, "vlr_hora": 5416.67},
     {"total_extras_diurnas": 33854.19, "total_extras_nocturnas": 0.0, "total_devengado": 1333854.19, "descuento_salud": 53354.17, "descuento_pension": 53354.17, "auxilio_transporte": 162000.0, "neto_pagar": 1389145.85}),
]

@pytest.mark.parametrize("case_id, entrada, esperado", casos, ids=[c[0] for c in casos])
def test_nomina_pro(case_id, entrada, esperado):
    if "error_esperado" in esperado:
        with pytest.raises(ValueError):
            liquidar_nomina(**entrada)
    else:
        resultado = liquidar_nomina(**entrada)
        for clave, valor in esperado.items():
            assert resultado[clave] == valor, f"Fallo en {case_id}: {clave}"