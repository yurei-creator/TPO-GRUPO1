from .Func_Rich import console, mostrar_mensaje, renderizar_tabla

def fila_a_diccionario(encabezados, fila):
    return dict(zip(encabezados, fila))

def obtener_nombre_categoria(id_cat, categorias):
    for c in categorias:
        if c[0] == str(id_cat):
            return c[1]
    return "Sin Categoría"

def obtener_categoria_por_id(id_cat, categorias):
    for c in categorias:
        if c[0] == str(id_cat):
            return c
    return None

def obtener_presupuesto_por_categoria(id_cat, presupuestos):
    for p in presupuestos:
        if p[1] == str(id_cat) and p[4] == "Activo":
            return p
    return None

def mostrar_categorias(categorias, encabezados):
    filas = []
    for c in categorias:
        filas.append([c[0], c[1], c[2], c[3]])
    renderizar_tabla(encabezados, filas, "Listado de Categorías")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def mostrar_presupuestos(presupuestos, categorias, encabezados):
    filas = []
    for p in presupuestos:
        nom_cat = obtener_nombre_categoria(p[1], categorias)
        monto_fmt = f"${float(p[3]):,.2f}"
        filas.append([p[0], nom_cat, p[2], monto_fmt, p[4]])
    
    encs = ["ID", "Categoría", "Período", "Monto Límite", "Estado"]
    renderizar_tabla(encs, filas, "Listado de Presupuestos")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def leer_lineas_recursivo(arch, matriz):
    '''Lee el archivo línea por línea de forma recursiva y agrega cada registro a la matriz.'''
    linea = arch.readline()
    if linea:  # caso base: cuando readline() devuelve "" se terminó el archivo
        if linea.strip():
            matriz.append(linea.strip().split("|"))
        leer_lineas_recursivo(arch, matriz)  # caso recursivo: sigue con la próxima línea

def cargar_matriz(archivo):
    matriz = []

    try:
        with open(archivo, "rt", encoding="utf-8") as arch:
            leer_lineas_recursivo(arch, matriz)
    except FileNotFoundError:
        mostrar_mensaje(f"No se encontró el archivo {archivo}.", "error")
    except OSError as error:
        mostrar_mensaje(f"No se pudo leer el archivo {archivo}: {error}", "error")
    except RecursionError:
        mostrar_mensaje(f"El archivo {archivo} tiene demasiadas líneas para leerlo de forma recursiva.", "error")

    return matriz