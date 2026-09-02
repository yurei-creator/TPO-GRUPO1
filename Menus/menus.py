
from Backup import (
    Table,
    console,
    mostrar_mensaje,
    pedir_texto_no_vacio,
    mostrar_categorias,
    consultar_categoria,
    agregar_categoria,
    modificar_categoria,
    eliminar_categoria,
    mostrar_presupuestos,
    consultar_presupuesto,
    agregar_presupuesto,
    modificar_presupuesto,
    eliminar_presupuesto,
    mostrar_gastos,
    consultar_gasto,
    agregar_gasto,
    modificar_gasto,
    eliminar_gasto,
)


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


def menu_categorias():
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
        opc = pedir_texto_no_vacio("Seleccione una opción: ")

        if opc == "1":
            mostrar_categorias()
        elif opc == "2":
            consultar_categoria()
        elif opc == "3":
            agregar_categoria()
        elif opc == "4":
            modificar_categoria()
        elif opc == "5":
            eliminar_categoria()
        elif opc == "0":
            activo = False
        else:
            mostrar_mensaje("Opción no válida.", "error")


def menu_presupuestos():
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
        opc = pedir_texto_no_vacio("Seleccione una opción: ")

        if opc == "1":
            mostrar_presupuestos()
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
        opc = pedir_texto_no_vacio("Seleccione una opción: ")

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


def menu_principal():
    ejecutando = True
    opciones = [
        "Gestión de Gastos (CRUD)",
        "Gestión de Presupuestos (CRUD)",
        "Gestión de Categorías (CRUD)",
        "Ver Todas las Tablas",
    ]
    while ejecutando:
        mostrar_menu("SISTEMA DE GESTION FINANCIERA", opciones)
        opcion = pedir_texto_no_vacio("Seleccione una opción: ")

        if opcion == "1":
            menu_gastos()
        elif opcion == "2":
            menu_presupuestos()
        elif opcion == "3":
            menu_categorias()
        elif opcion == "4":
            mostrar_categorias()
            mostrar_presupuestos()
            mostrar_gastos()
        elif opcion == "0":
            mostrar_mensaje("¡Gracias por utilizar el sistema! Hasta luego.", "info")
            ejecutando = False
        else:
            mostrar_mensaje("Opción no válida. Intente nuevamente.", "error")
