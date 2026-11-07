# python -m pytest -v

from Crud.Crud_Categorias.Crud_Cat import obtener_ultimo_codigo
from Datos.Datos import encabezadosC
from Func.Func_Matriz import fila_a_diccionario, obtener_categoria_por_id, cargar_matriz
from Func.Func_val import seleccionar_categoria_id

# datos de prueba
categorias_prueba = [
    ["1", "Alimentos", "Comida y bebida", "Activo"],
    ["2", "Transporte", "Colectivo y tren", "Activo"],
    ["3", "Ocio", "Salidas y cine", "Inactivo"],
]


# buscar una categoría por su id

def test_buscar_categoria_existente():
    assert obtener_categoria_por_id("2", categorias_prueba) == categorias_prueba[1]

def test_buscar_categoria_con_id_numerico():
    # el id se puede pasar como número o como texto
    assert obtener_categoria_por_id(1, categorias_prueba) == categorias_prueba[0]

def test_buscar_categoria_inactiva():
    # un gasto viejo puede seguir usando esa categoría
    assert obtener_categoria_por_id("3", categorias_prueba) == categorias_prueba[2]

def test_buscar_categoria_inexistente():
    assert obtener_categoria_por_id("99", categorias_prueba) == None


# seleccionar una categoría cuando no hay ninguna disponible

def test_seleccionar_sin_categorias():
    assert seleccionar_categoria_id([]) == None

def test_seleccionar_con_todas_inactivas():
    assert seleccionar_categoria_id([categorias_prueba[2]]) == None


# pasar una fila de categoría a diccionario

def test_fila_de_categoria_a_diccionario():
    esperado = {"ID": "1", "Nombre": "Alimentos", "Descripcion": "Comida y bebida", "Estado": "Activo"}
    assert fila_a_diccionario(encabezadosC, categorias_prueba[0]) == esperado


# obtener el último código cuando no existe el archivo

def test_ultimo_codigo_sin_archivo():
    assert obtener_ultimo_codigo("archivo_que_no_existe.txt") == ("1", [])


# leer el archivo de categorías de forma recursiva

def test_cargar_matriz_sin_archivo():
    assert cargar_matriz("archivo_que_no_existe.txt") == []

def test_cargar_matriz_lee_todas_las_columnas():
    categorias = cargar_matriz("Datos/categorias.txt")
    assert len(categorias) > 0
    # cada fila tiene ID, nombre, descripción y estado
    for fila in categorias:
        assert len(fila) == 4
