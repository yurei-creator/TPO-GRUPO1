# python -m pytest -v

from Func.Func_val import es_fecha_valida, fecha_a_numero, filtrar_por_fechas_recursivo
from Func.Func_Matriz import obtener_nombre_categoria

# datos de prueba
gastos_prueba = [
    {"id": "1", "fecha": "01/08/2026", "monto": 12500.0, "categoria_id": "1", "descripcion": "Supermercado", "estado": "Activo"},
    {"id": "2", "fecha": "15/08/2026", "monto": 5000.0, "categoria_id": "2", "descripcion": "Colectivo", "estado": "Activo"},
    {"id": "3", "fecha": "20/08/2026", "monto": 3000.0, "categoria_id": "1", "descripcion": "Verdulería", "estado": "Inactivo"},
    {"id": "4", "fecha": "05/09/2026", "monto": 8000.0, "categoria_id": "2", "descripcion": "Tren", "estado": "Activo"},
]

categorias_prueba = [
    ["1", "Alimentos", "Comida y bebida", "Activo"],
    ["2", "Transporte", "Colectivo y tren", "Activo"],
]


# validar la fecha de un gasto

def test_fecha_valida():
    assert es_fecha_valida("15/08/2026") == True

def test_fecha_con_formato_incorrecto():
    assert es_fecha_valida("2026-08-15") == False

def test_fecha_con_mes_inexistente():
    assert es_fecha_valida("15/13/2026") == False

def test_fecha_con_dia_inexistente():
    # abril tiene 30 días
    assert es_fecha_valida("31/04/2026") == False

def test_29_de_febrero_en_anio_bisiesto():
    assert es_fecha_valida("29/02/2024") == True

def test_29_de_febrero_en_anio_no_bisiesto():
    assert es_fecha_valida("29/02/2026") == False



# filtrar gastos por rango de fechas

def test_filtrar_gastos_dentro_del_rango():
    resultado = filtrar_por_fechas_recursivo(gastos_prueba, "01/09/2026", "30/09/2026")
    assert resultado == [gastos_prueba[3]]

def test_filtrar_incluye_las_fechas_limite():
    resultado = filtrar_por_fechas_recursivo(gastos_prueba, "01/08/2026", "15/08/2026")
    assert resultado == [gastos_prueba[0], gastos_prueba[1]]

def test_filtrar_no_incluye_gastos_inactivos():
    # el rango es justo la fecha del gasto 3, que está Inactivo
    resultado = filtrar_por_fechas_recursivo(gastos_prueba, "20/08/2026", "20/08/2026")
    assert resultado == []

def test_filtrar_rango_sin_gastos():
    resultado = filtrar_por_fechas_recursivo(gastos_prueba, "01/01/2020", "31/12/2020")
    assert resultado == []

def test_filtrar_rango_invertido():
    # la fecha inicial es posterior a la final
    resultado = filtrar_por_fechas_recursivo(gastos_prueba, "31/08/2026", "01/08/2026")
    assert resultado == []

def test_filtrar_lista_vacia():
    resultado = filtrar_por_fechas_recursivo([], "01/08/2026", "31/08/2026")
    assert resultado == []


# obtener el nombre de la categoría de un gasto

def test_nombre_de_categoria_existente():
    assert obtener_nombre_categoria("2", categorias_prueba) == "Transporte"

def test_nombre_de_categoria_inexistente():
    assert obtener_nombre_categoria("99", categorias_prueba) == "Sin Categoría"
