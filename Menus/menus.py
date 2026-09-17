from Func.Func_Rich import (
    console, 
    mostrar_mensaje, 
    Table
)
from Func.Func_Matriz import (
    mostrar_categorias,
    mostrar_presupuestos,
    mostrar_gastos,
    obtener_matriz
)
from Func.Func_val import (
    pedir_opcion_menu,
)
from Crud.Crud_Cat import (
    consultar_categoria,
    agregar_categoria,
    modificar_categoria,
    eliminar_categoria,
)
from Crud.Crud_Usuarios import verificar_permiso

from Crud.Crud_Gast import *

from Crud.Crud_Pres import *


def mostrar_menu(titulo, opciones):
    tabla_menu = Table(
        title=f"[bold cyan]{titulo}[/bold cyan]",
        show_header=True,
        header_style="bold magenta",
        border_style="bright_blue",
    )
    tabla_menu.add_column("Opción", justify="center", style="bold yellow")
    tabla_menu.add_column("Descripción", justify="left", style="white")

    for i in range(len(opciones)):
        numero_opcion = str(i + 1)
        nombre_opcion = opciones[i]
        tabla_menu.add_row(numero_opcion, nombre_opcion)

    tabla_menu.add_row("0", "Salir")

    console.print()
    console.print(tabla_menu)
    console.print()


def menu_categorias(matriz,encabezado):
    activo = True
    opciones = [
        "Mostrar categorías",
        "Consultar / Buscar categoría",
        "Agregar categoría",
        "Modificar categoría",
        "Baja lógica de categoría",
    ]
    while activo:
        mostrar_menu("GESTIÓN DE CATEGORÍAS", opciones)
        opc = pedir_opcion_menu("Seleccione una opción:", ["0","1","2","3","4","5"])

        if opc == "1":
            mostrar_categorias(matriz,encabezado)
        elif opc == "2":
            consultar_categoria(matriz,encabezado)
        elif opc == "3":
            agregar_categoria(matriz)
        elif opc == "4":
            modificar_categoria(matriz)
        elif opc == "5":
            eliminar_categoria()
        elif opc == "0":
            activo = False
        else:
            mostrar_mensaje("Opción no válida.", "error")


def menu_presupuestos(matrizP,encabezadoP,matrizG):
    activo = True
    opciones = [
        "Mostrar presupuestos",
        "Consultar / Buscar presupuesto",
        "Agregar presupuesto",
        "Modificar presupuesto",
        "Baja lógica de presupuesto",
    ]
    while activo:
        mostrar_menu("GESTIÓN DE PRESUPUESTOS", opciones)
        opc = pedir_opcion_menu("Seleccione una opción:", ["0","1","2","3","4","5"])

        if opc == "1":
            mostrar_presupuestos(matrizP,encabezadoP,matrizG)
        elif opc == "2":
            consultar_presupuesto()
        elif opc == "3":
            agregar_presupuesto()
        elif opc == "4":
            modificar_presupuesto()
        elif opc == "5":
            eliminar_presupuesto()
        elif opc == "0":
            activo = False
        else:
            mostrar_mensaje("Opción no válida.", "error")


def menu_gastos():
    activo = True
    opciones = [
        "Mostrar gastos",
        "Consultar / Buscar gasto",
        "Agregar gasto",
        "Modificar gasto",
        "Baja lógica de gasto",
    ]
    while activo:
        mostrar_menu("GESTIÓN DE GASTOS", opciones)
        opc = pedir_opcion_menu("Seleccione una opción:", ["0","1","2","3","4","5"])

        if opc == "1":
            mostrar_gastos()
        elif opc == "2":
            consultar_gasto()
        elif opc == "3":
            agregar_gasto()
        elif opc == "4":
            modificar_gasto()
        elif opc == "5":
            eliminar_gasto()
        elif opc == "0":
            activo = False
        else:
            mostrar_mensaje("Opción no válida.", "error")


def menu_principal(usuario,categoria,presupuestos,gastos,encabezadoC,encabezadoP,encabezadoG):
    ejecutando = True

    matriz_presupuestos = obtener_matriz(presupuestos)
    matriz_categorias = obtener_matriz(categoria)

    modulos = [
        ("gastos", "Gestión de Gastos (CRUD)"),
        ("presupuestos", "Gestión de Presupuestos (CRUD)"),
        ("categorias", "Gestión de Categorías (CRUD)"),
        ("reportes", "Ver Todas las Tablas"),
    ]

    while ejecutando:
        disponibles = []
        for i in range(len(modulos)):
            permiso, texto = modulos[i]
            if verificar_permiso(usuario, permiso):
                disponibles.append((permiso, texto))

        opciones_texto = [d[1] for d in disponibles]
        mostrar_menu("SISTEMA DE GESTION FINANCIERA", opciones_texto)

        opciones_validas = ["0"]
        for i in range(len(disponibles)):
            opciones_validas.append(str(i + 1))

        opcion = pedir_opcion_menu("Seleccione una opción:", opciones_validas)

        if opcion == "0":
            mostrar_mensaje("¡Gracias por utilizar el sistema! Hasta luego.", "info")
            ejecutando = False
        else:
            indice = int(opcion) - 1
            permiso_elegido = disponibles[indice][0]
            if permiso_elegido == "gastos":
                matriz_gastos = obtener_matriz(gastos)
                menu_gastos(matriz_gastos,encabezadoG)
            elif permiso_elegido == "presupuestos":
                menu_presupuestos(matriz_presupuestos,encabezadoP,matriz_categorias)
            elif permiso_elegido == "categorias":
                menu_categorias(matriz_categorias,encabezadoC)
            elif permiso_elegido == "reportes":
                matriz_gastos = obtener_matriz(gastos)
                mostrar_categorias(matriz_categorias,encabezadoC)
                mostrar_presupuestos(matriz_presupuestos,encabezadoP)
                mostrar_gastos(matriz_gastos,encabezadoG)
