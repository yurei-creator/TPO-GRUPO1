from Func_Rich import console, mostrar_mensaje, renderizar_tabla, Table
from Func_Val import obtener_nombre_categoria, obtener_periodo_presupuesto

from datosprincipales import (
    NombreC, EstadoC, DescripcionC, 
    Periodo_Presupuesto, EstadoP, Id_CategoriaP, Monto_limite, 
    NombreG, EstadoG, Id_CatGasto, Id_PresGasto, MontoG, FechaG, DescripcionG
)

def obtener_matriz(lista):
    matriz = []
    total_filas = len(lista[0])
    total_columnas = len(lista)
    for col in range(total_filas):
        fila = []
        for fil in range(total_columnas):
            fila.append(lista[fil][col])
        matriz.append(fila)
    return matriz

def mostrar_matriz(matriz, encabezados, titulo_tabla):
    if not matriz:
        mostrar_mensaje("No hay datos cargados.", tipo="error")
        return

    filas_activas = [fila for fila in matriz if str(fila[-1]).upper() == "ACTIVO"]

    if not filas_activas:
        mostrar_mensaje("No hay registros activos para mostrar.", tipo="alerta")
        return

    cant_encabezados = len(encabezados)
    cant_columnas_datos = len(matriz[0]) - 1
    total_columnas = (
        cant_encabezados
        if cant_encabezados < cant_columnas_datos
        else cant_columnas_datos
    )

    tabla = Table(
        title=f"[bold cyan]{titulo_tabla}[/bold cyan]",
        header_style="bold magenta",
        border_style="bright_blue",
    )

    for i in range(total_columnas):
        tabla.add_column(encabezados[i], justify="left", style="white")

    for fila in filas_activas:
        valores = [str(fila[i]) for i in range(total_columnas)]
        tabla.add_row(*valores)

    console.print()
    console.print(tabla)
    console.print()
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def mostrar_categorias():
    encabezados = ["Categoría", "Descripción"]
    filas = []
    for i in range(len(NombreC)):
        if str(EstadoC[i]).upper() == "ACTIVO":
            filas.append([NombreC[i], DescripcionC[i]])
    renderizar_tabla(encabezados, filas, "Listado de Categorías")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def mostrar_presupuestos():
    encabezados = ["Período", "Categoría Asignada", "Monto Límite"]
    filas = []
    for i in range(len(Periodo_Presupuesto)):
        if str(EstadoP[i]).upper() == "ACTIVO":
            nombre_cat = obtener_nombre_categoria(Id_CategoriaP[i])
            monto_fmt = f"${float(Monto_limite[i]):.2f}"
            filas.append([Periodo_Presupuesto[i], nombre_cat, monto_fmt])
    renderizar_tabla(encabezados, filas, "Listado de Presupuestos")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def mostrar_gastos():
    encabezados = ["Gasto", "Fecha", "Monto", "Descripción", "Categoría", "Período Asignado"]
    filas = []
    for i in range(len(NombreG)):
        if str(EstadoG[i]).upper() == "ACTIVO":
            nombre_cat = obtener_nombre_categoria(Id_CatGasto[i])
            periodo_pres = obtener_periodo_presupuesto(Id_PresGasto[i])
            monto_fmt = f"$USD {float(MontoG[i]):,.2f}"
            filas.append([
                NombreG[i],
                FechaG[i],
                monto_fmt,
                DescripcionG[i],
                nombre_cat,
                periodo_pres
            ])
    renderizar_tabla(encabezados, filas, "Control General de Gastos")
    console.input("[dim]Presione ENTER para continuar...[/dim]")