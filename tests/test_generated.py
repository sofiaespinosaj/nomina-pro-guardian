import pytest
from src.engine import liquidar_nomina

def test_cp01():
    r = liquidar_nomina(2600000.0, 0, 0, 10833.33)
    assert r["salario_base"] == 2600000.0
    assert r["total_extras_diurnas"] == 0.0
    assert r["total_extras_nocturnas"] == 0.0
    assert r["total_devengado"] == 2600000.0
    assert r["descuento_salud"] == pytest.approx(104000.0, abs=0.1)
    assert r["descuento_pension"] == pytest.approx(104000.0, abs=0.1)
    assert r["auxilio_transporte"] == pytest.approx(162000.0, abs=0.1)
    assert r["neto_pagar"] == pytest.approx(2554000.0, abs=0.1)

def test_cp02():
    with pytest.raises(ValueError):
        liquidar_nomina(1500000.0, -5, 0, 6250.0)

def test_cp03():
    r = liquidar_nomina(2000000.0, 0, 0, 8333.33)
    assert r["total_devengado"] == pytest.approx(2000000.0, abs=0.1)
    assert r["descuento_salud"] == pytest.approx(80000.0, abs=0.1)
    assert r["descuento_pension"] == pytest.approx(80000.0, abs=0.1)

def test_cp04():
    r = liquidar_nomina(1300000.0, 4, 2, 5416.67)
    assert r["total_extras_diurnas"] == pytest.approx(27083.35, abs=0.1)
    assert r["total_extras_nocturnas"] == pytest.approx(18958.35, abs=0.1)
    assert r["total_devengado"] == pytest.approx(1346041.70, abs=0.1)

def test_cp05():
    r = liquidar_nomina(3000000.0, 0, 0, 12500.0)
    assert r["auxilio_transporte"] == 0.0
    assert r["neto_pagar"] == pytest.approx(2760000.0, abs=0.1)

def test_cp06():
    r = liquidar_nomina(1300000.0, 0, 0, 5416.67)
    assert r["total_devengado"] == pytest.approx(1300000.0, abs=0.1)
    assert r["auxilio_transporte"] == pytest.approx(162000.0, abs=0.1)
    assert r["neto_pagar"] == pytest.approx(1358000.0, abs=0.1)

def test_cp07():
    with pytest.raises(ValueError):
        liquidar_nomina(1200000.0, 0, 0, 5000.0)

def test_cp08():
    with pytest.raises(ValueError):
        liquidar_nomina(1600000.0, 10, 0, 11666.67)

def test_cp09():
    r = liquidar_nomina(2500000.0, 0, 0, 10416.67)
    assert r["total_devengado"] == pytest.approx(2500000.0, abs=0.1)
    assert r["descuento_pension"] == pytest.approx(100000.0, abs=0.1)

def test_cp10():
    r = liquidar_nomina(1300000.0, 4, 2, 5416.67)
    assert r["salario_base"] == pytest.approx(1300000.0, abs=0.1)
    assert r["total_extras_diurnas"] == pytest.approx(27083.35, abs=0.1)
    assert r["total_extras_nocturnas"] == pytest.approx(18958.35, abs=0.1)
    assert r["total_devengado"] == pytest.approx(1346041.70, abs=0.1)
    assert r["descuento_salud"] == pytest.approx(53841.67, abs=0.1)
    assert r["descuento_pension"] == pytest.approx(53841.67, abs=0.1)
    assert r["auxilio_transporte"] == pytest.approx(162000.0, abs=0.1)
    assert r["neto_pagar"] == pytest.approx(1400358.36, abs=0.1)

def test_cp11():
    r = liquidar_nomina(2800000.0, 12, 8, 11666.67)
    assert r["salario_base"] == pytest.approx(2800000.0, abs=0.1)
    assert r["total_extras_diurnas"] == pytest.approx(175000.05, abs=0.1)
    assert r["total_extras_nocturnas"] == pytest.approx(163333.38, abs=0.1)
    assert r["total_devengado"] == pytest.approx(3138333.43, abs=0.1)
    assert r["descuento_salud"] == pytest.approx(125533.34, abs=0.1)
    assert r["descuento_pension"] == pytest.approx(125533.34, abs=0.1)
    assert r["auxilio_transporte"] == 0.0
    assert r["neto_pagar"] == pytest.approx(2887266.76, abs=0.1)

def test_cp12():
    r = liquidar_nomina(1300000.0, 5, 0, 5416.67)
    assert r["salario_base"] == pytest.approx(1300000.0, abs=0.1)
    assert r["total_extras_diurnas"] == pytest.approx(33854.19, abs=0.1)
    assert r["total_extras_nocturnas"] == 0.0
    assert r["total_devengado"] == pytest.approx(1333854.19, abs=0.1)
    assert r["descuento_salud"] == pytest.approx(53354.17, abs=0.1)
    assert r["descuento_pension"] == pytest.approx(53354.17, abs=0.1)
    assert r["auxilio_transporte"] == pytest.approx(162000.0, abs=0.1)
    assert r["neto_pagar"] == pytest.approx(1389145.85, abs=0.1)