import pytest
from src.engine import liquidar_nomina

def test_cp01():
    entrada = {
        "salario_base": 2600000.0,
        "horas_extras_diurnas": 0,
        "horas_extras_nocturnas": 0,
        "vlr_hora": 10833.33
    }
    esperado = {
        "salario_base": 2600000.0,
        "total_extras_diurnas": 0.0,
        "total_extras_nocturnas": 0.0,
        "total_devengado": 2600000.0,
        "descuento_salud": 104000.0,
        "descuento_pension": 104000.0,
        "auxilio_transporte": 162000.0,
        "neto_pagar": 2554000.0
    }
    assert liquidar_nomina(**entrada) == esperado

def test_cp02():
    entrada = {
        "salario_base": 1500000.0,
        "horas_extras_diurnas": -5,
        "horas_extras_nocturnas": 0,
        "vlr_hora": 6250.0
    }
    with pytest.raises(ValueError) as exc_info:
        liquidar_nomina(**entrada)
    assert "no puede ser negativa" in str(exc_info.value)

def test_cp03():
    entrada = {
        "salario_base": 2000000.0,
        "horas_extras_diurnas": 0,
        "horas_extras_nocturnas": 0,
        "vlr_hora": 8333.33
    }
    esperado = {
        "salario_base": 2000000.0,
        "total_extras_diurnas": 0.0,
        "total_extras_nocturnas": 0.0,
        "total_devengado": 2000000.0,
        "descuento_salud": 80000.0,
        "descuento_pension": 80000.0,
        "auxilio_transporte": 162000.0,
        "neto_pagar": 2002000.0
    }
    assert liquidar_nomina(**entrada) == esperado

def test_cp04():
    entrada = {
        "salario_base": 1300000.0,
        "horas_extras_diurnas": 4,
        "horas_extras_nocturnas": 2,
        "vlr_hora": 5416.67
    }
    esperado = {
        "salario_base": 1300000.0,
        "total_extras_diurnas": 27083.35,
        "total_extras_nocturnas": 18958.35,
        "total_devengado": 1346041.70,
        "descuento_salud": 53841.67,
        "descuento_pension": 53841.67,
        "auxilio_transporte": 162000.0,
        "neto_pagar": 1400358.36
    }
    assert liquidar_nomina(**entrada) == esperado

def test_cp05():
    entrada = {
        "salario_base": 3000000.0,
        "horas_extras_diurnas": 0,
        "horas_extras_nocturnas": 0,
        "vlr_hora": 12500.0
    }
    esperado = {
        "salario_base": 3000000.0,
        "total_extras_diurnas": 0.0,
        "total_extras_nocturnas": 0.0,
        "total_devengado": 3000000.0,
        "descuento_salud": 120000.0,
        "descuento_pension": 120000.0,
        "auxilio_transporte": 0.0,
        "neto_pagar": 2760000.0
    }
    assert liquidar_nomina(**entrada) == esperado

def test_cp06():
    entrada = {
        "salario_base": 1300000.0,
        "horas_extras_diurnas": 0,
        "horas_extras_nocturnas": 0,
        "vlr_hora": 5416.67
    }
    esperado = {
        "salario_base": 1300000.0,
        "total_extras_diurnas": 0.0,
        "total_extras_nocturnas": 0.0,
        "total_devengado": 1300000.0,
        "descuento_salud": 52000.0,
        "descuento_pension": 52000.0,
        "auxilio_transporte": 162000.0,
        "neto_pagar": 1358000.0
    }
    assert liquidar_nomina(**entrada) == esperado

def test_cp07():
    entrada = {
        "salario_base": 1200000.0,
        "horas_extras_diurnas": 0,
        "horas_extras_nocturnas": 0,
        "vlr_hora": 5000.0
    }
    with pytest.raises(ValueError) as exc_info:
        liquidar_nomina(**entrada)
    assert "inferior al mínimo legal" in str(exc_info.value)

def test_cp08():
    entrada = {
        "salario_base": 1600000.0,
        "horas_extras_diurnas": 10,
        "horas_extras_nocturnas": 0,
        "vlr_hora": 0.0
    }
    with pytest.raises(ValueError) as exc_info:
        liquidar_nomina(**entrada)
    assert "debe ser estrictamente mayor a cero" in str(exc_info.value)

def test_cp09():
    entrada = {
        "salario_base": 2500000.0,
        "horas_extras_diurnas": 0,
        "horas_extras_nocturnas": 0,
        "vlr_hora": 10416.67
    }
    esperado = {
        "salario_base": 2500000.0,
        "total_extras_diurnas": 0.0,
        "total_extras_nocturnas": 0.0,
        "total_devengado": 2500000.0,
        "descuento_salud": 100000.0,
        "descuento_pension": 100000.0,
        "auxilio_transporte": 162000.0,
        "neto_pagar": 2462000.0
    }
    assert liquidar_nomina(**entrada) == esperado

def test_cp10():
    entrada = {
        "salario_base": 1300000.0,
        "horas_extras_diurnas": 4,
        "horas_extras_nocturnas": 2,
        "vlr_hora": 5416.67
    }
    esperado = {
        "salario_base": 1300000.0,
        "total_extras_diurnas": 27083.35,
        "total_extras_nocturnas": 18958.35,
        "total_devengado": 1346041.70,
        "descuento_salud": 53841.67,
        "descuento_pension": 53841.67,
        "auxilio_transporte": 162000.0,
        "neto_pagar": 1400358.36
    }
    assert liquidar_nomina(**entrada) == esperado

def test_cp11():
    entrada = {
        "salario_base": 2800000.0,
        "horas_extras_diurnas": 12,
        "horas_extras_nocturnas": 8,
        "vlr_hora": 11666.67
    }
    esperado = {
        "salario_base": 2800000.0,
        "total_extras_diurnas": 175000.05,
        "total_extras_nocturnas": 163333.38,
        "total_devengado": 3138333.43,
        "descuento_salud": 125533.34,
        "descuento_pension": 125533.34,
        "auxilio_transporte": 0.0,
        "neto_pagar": 2887266.76
    }
    assert liquidar_nomina(**entrada) == esperado

def test_cp12():
    entrada = {
        "salario_base": 1300000.0,
        "horas_extras_diurnas": 5,
        "horas_extras_nocturnas": 0,
        "vlr_hora": 5416.67
    }
    esperado = {
        "salario_base": 1300000.0,
        "total_extras_diurnas": 33854.19,
        "total_extras_nocturnas": 0.0,
        "total_devengado": 1333854.19,
        "descuento_salud": 53354.17,
        "descuento_pension": 53354.17,
        "auxilio_transporte": 162000.0,
        "neto_pagar": 1389145.85
    }
    assert liquidar_nomina(**entrada) == esperado