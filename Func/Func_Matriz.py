from .Func_Rich import console, mostrar_mensaje, renderizar_tabla, Table
from .Func_val import obtener_nombre_categoria, obtener_periodo_presupuesto
from .Auxiliares import obtener_nombre_categoria as Auxiliar_nombre

from Datos.Datos import *

#buenas practicas, etc.
#Pq hardcodeamos los encabezados? xD


# M.Categoria = [[[ID],[NOMBRE],[DESCRIPCION],[ESTADO]]]
# M.Presupuesto = [[[ID pk], [ID CAT FK], [MONTOLIMITE], [PERIODO], [ESTADO]]]
presupuestos = [Id_Presupuesto, Id_Categoria, Monto_limite,Periodo_Presupuesto, EstadoP]
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

def mostrar_categorias(matriz, encabezados):
    # Deberiamos poner un filtro de Activo/Inactivo aca? No creo, como ve el usuario si existen categorias inactivas
    #filas = []
    #for i in range(len(matriz)):
    #    if str(matriz[i][3]).upper() == "ACTIVO":
    #
    #         filas.append([matriz[i][0], matriz[i][1], matriz[i][2], matriz[i][3]])
    #
    renderizar_tabla(encabezados, matriz, "Listado de Categorías")

    console.input("[dim]Presione ENTER para continuar...[/dim]")

def mostrar_presupuestos(matriz,encabezados,matriz_categoria):
    filas = []
    for i in range(len(matriz)):
        if str(matriz[i][4]).upper() == "ACTIVO":
            nombre_cat = obtener_nombre_categoria(matriz[i][1])
            
            monto_fmt = f"${float(matriz[i][2]):.2f}"
            filas.append([matriz[i][0],matriz[i][1], nombre_cat, monto_fmt, matriz[i][4]])
    renderizar_tabla(encabezados, filas, "Listado de Presupuestos")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def mostrar_gastos():
    encabezados = ["Gasto", "Fecha", "Monto", "Descripción", "Categoría", "Período Asignado", "Estado"]
    filas = []
    for i in range(len(NombreG)):
        if EstadoG[i] == True:
            nombre_cat = obtener_nombre_categoria(Id_CatGasto[i])
            periodo_pres = obtener_periodo_presupuesto(Id_PresGasto[i])
            monto_fmt = f"$USD {float(MontoG[i]):,.2f}"
            filas.append([
                NombreG[i],
                FechaG[i],
                monto_fmt,
                DescripcionG[i],
                nombre_cat,
                periodo_pres,
                "Activo"
            ])
    print(gastos)       
    renderizar_tabla(encabezados, filas, "Control General de Gastos")
    console.input("[dim]Presione ENTER para continuar...[/dim]")