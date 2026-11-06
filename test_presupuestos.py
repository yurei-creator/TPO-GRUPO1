# python -m pytest -v

from Datos.Datos import encabezadosP
from Func.Func_Matriz import fila_a_diccionario, obtener_presupuesto_por_categoria

# datos de prueba:
presupuestos_prueba = [
    ["1", "1", "01/08/2026-31/08/2026", "50000.0", "Activo"],
    ["2", "2", "01/08/2026-31/08/2026", "20000.0", "Inactivo"],
    ["3", "3", "01/07/2026-31/07/2026", "15000.0", "Inactivo"],
    ["4", "3", "01/08/2026-31/08/2026", "18000.0", "Activo"],
]


# buscar el presupuesto de una categoría

def test_buscar_presupuesto_activo():
    assert obtener_presupuesto_por_categoria("1", presupuestos_prueba) == presupuestos_prueba[0]

def test_buscar_presupuesto_con_id_numerico():
    # el id se puede pasar como número o como texto
    assert obtener_presupuesto_por_categoria(1, presupuestos_prueba) == presupuestos_prueba[0]

def test_no_devuelve_presupuesto_inactivo():
    assert obtener_presupuesto_por_categoria("2", presupuestos_prueba) == None

def test_elige_el_activo_si_la_categoria_tiene_varios():
    # la categoría 3 tiene uno Inactivo y otro Activo
    assert obtener_presupuesto_por_categoria("3", presupuestos_prueba) == presupuestos_prueba[3]

def test_categoria_sin_presupuesto():
    assert obtener_presupuesto_por_categoria("99", presupuestos_prueba) == None

def test_sin_presupuestos_cargados():
    assert obtener_presupuesto_por_categoria("1", []) == None


# pasar una fila de presupuesto a diccionario

def test_fila_de_presupuesto_a_diccionario():
    esperado = {
        "ID": "1",
        "ID_Categoria": "1",
        "Periodo": "01/08/2026-31/08/2026",
        "Monto Limite": "50000.0",
        "Estado": "Activo",
    }
    assert fila_a_diccionario(encabezadosP, presupuestos_prueba[0]) == esperado
