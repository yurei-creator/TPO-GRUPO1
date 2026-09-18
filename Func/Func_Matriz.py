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

def mostrar_gastos(gastos, categorias, encabezados):
    filas = []
    for g in gastos:
        nom_cat = obtener_nombre_categoria(g[3], categorias)
        monto_fmt = f"${float(g[2]):,.2f}"
        filas.append([g[0], g[1], monto_fmt, nom_cat, g[4], g[5]])
    
    encs = ["ID", "Fecha", "Monto", "Categoría", "Descripción", "Estado"]
    renderizar_tabla(encs, filas, "Control General de Gastos")
    console.input("[dim]Presione ENTER para continuar...[/dim]")