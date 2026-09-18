from Func.Func_Rich import console, mostrar_mensaje, renderizar_tabla
from Func.Func_val import pedir_texto_no_vacio, pedir_opcional, pedir_opcion_menu
from Func.Func_Matriz import fila_a_diccionario
from rich.table import Table

def agregar_categoria(categoria):
    console.print("\n[bold green]--- [C] AGREGAR NUEVA CATEGORÍA ---[/bold green]")
    ids_existentes = [int(c[0]) for c in categoria if c[0].isdigit()]
    nuevo_id = str(max(ids_existentes) + 1) if ids_existentes else "1"

    nombre = pedir_texto_no_vacio("Ingrese nombre de la categoría:")
    
    # Validar que no exista categoría activa con el mismo nombre
    for c in categoria:
        if c[1].lower() == nombre.lower() and c[3] == "Activo":
            mostrar_mensaje(f"Ya existe una categoría activa con el nombre '{nombre}'.", "alerta")
            console.input("[dim]Presione ENTER para continuar...[/dim]")
            return

    descripcion = pedir_texto_no_vacio("Ingrese descripción:")
    categoria.append([nuevo_id, nombre, descripcion, "Activo"])

    mostrar_mensaje(f"Categoría '{nombre}' agregada exitosamente con ID: {nuevo_id}", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def consultar_categoria(categoria, gastos, presupuestos, encabezadosC, encabezadosG):
    console.print("\n[bold yellow]--- [R] CONSULTAR / BUSCAR CATEGORÍA ---[/bold yellow]")
    if not categoria:
        mostrar_mensaje("No hay categorías registradas en el sistema.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    busqueda = pedir_texto_no_vacio("Ingrese término de búsqueda (ID o Nombre):").lower()
    coincidencias = []

    for c in categoria:
        if busqueda == c[0].lower() or busqueda in c[1].lower():
            coincidencias.append(c)

    if not coincidencias:
        mostrar_mensaje("No se encontraron coincidencias para la búsqueda.", "alerta")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    for c in coincidencias:
        # Uso de dict(zip(...)) visto en Clase 6
        cat_dict = fila_a_diccionario(encabezadosC, c)
        
        console.print(f"\n[bold cyan]Ficha de la Categoría ID {cat_dict['ID']}:[/bold cyan]")
        console.print(f"  • [bold white]Nombre:[/bold white] {cat_dict['Nombre']}")
        console.print(f"  • [bold white]Descripción:[/bold white] {cat_dict['Descripcion']}")
        console.print(f"  • [bold white]Estado:[/bold white] {cat_dict['Estado']}")

        # Consulta de datos relacionados en la Entidad B (Presupuestos y Gastos)
        pres_relacionado = None
        for p in presupuestos:
            if p[1] == c[0] and p[4] == "Activo":
                pres_relacionado = p
                break

        gastos_relacionados = [g for g in gastos if g[3] == c[0] and g[5] == "Activo"]
        total_gastado = sum([float(g[2]) for g in gastos_relacionados])

        if pres_relacionado:
            limite = float(pres_relacionado[3])
            saldo = limite - total_gastado
            console.print(f"  • [bold white]Presupuesto Asignado:[/bold white] ${limite:,.2f} (Período: {pres_relacionado[2]})")
            console.print(f"  • [bold white]Gasto Real Acumulado:[/bold white] ${total_gastado:,.2f}")
            if saldo >= 0:
                console.print(f"  • [bold green]Saldo Disponible:[/bold green] ${saldo:,.2f}")
            else:
                console.print(f"  • [bold red]Excedido por:[/bold red] ${abs(saldo):,.2f}")
        else:
            console.print(f"  • [bold yellow]Presupuesto:[/bold yellow] Sin presupuesto activo asignado.")
            console.print(f"  • [bold white]Gasto Total Acumulado:[/bold white] ${total_gastado:,.2f}")

        if gastos_relacionados:
            console.print(f"\n[dim]Gastos asociados a '{c[1]}' ({len(gastos_relacionados)} registro/s):[/dim]")
            tabla = Table(header_style="bold magenta", border_style="bright_blue")
            tabla.add_column("ID Gasto", justify="center")
            tabla.add_column("Fecha", justify="center")
            tabla.add_column("Monto", justify="right", style="green")
            tabla.add_column("Descripción", style="white")

            for g in gastos_relacionados:
                tabla.add_row(g[0], g[1], f"${float(g[2]):,.2f}", g[4])
            console.print(tabla)
        else:
            console.print("[dim]No hay gastos activos asociados a esta categoría.[/dim]")

    console.print()
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def modificar_categoria(categoria):
    console.print("\n[bold blue]--- [U] MODIFICAR CATEGORÍA ---[/bold blue]")
    activas = [c for c in categoria if c[3] == "Activo"]
    if not activas:
        mostrar_mensaje("No hay categorías activas para modificar.", "alerta")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    console.print("Seleccione la categoría a modificar:")
    for i in range(len(activas)):
        c = activas[i]
        console.print(f"  [yellow]{i + 1}[/yellow]. ID {c[0]} - {c[1]} [dim]({c[2]})[/dim]")

    opciones = [str(i + 1) for i in range(len(activas))]
    opciones.append("0")
    opc = pedir_opcion_menu("Número de categoría a modificar (0 para cancelar):", opciones)
    if opc == "0":
        return

    idx_activa = int(opc) - 1
    cat_seleccionada = activas[idx_activa]

    console.print(f"\n[dim]Modificando '{cat_seleccionada[1]}' (ENTER para conservar valor):[/dim]")
    cat_seleccionada[1] = pedir_opcional("Nuevo nombre", cat_seleccionada[1])
    cat_seleccionada[2] = pedir_opcional("Nueva descripción", cat_seleccionada[2])

    cambiar_est = pedir_texto_no_vacio(f"¿Desea cambiar el estado actual ({cat_seleccionada[3]})? (s/n):").lower()
    if cambiar_est == "s":
        cat_seleccionada[3] = "Inactivo" if cat_seleccionada[3] == "Activo" else "Activo"
        mostrar_mensaje(f"Estado actualizado a: {cat_seleccionada[3]}", "info")

    mostrar_mensaje("Categoría actualizada correctamente.", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def eliminar_categoria(categoria):
    console.print("\n[bold red]--- [D] BAJA / REACTIVACIÓN LÓGICA DE CATEGORÍA ---[/bold red]")
    if not categoria:
        mostrar_mensaje("No hay categorías registradas.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    console.print("Listado general de categorías:")
    for i in range(len(categoria)):
        c = categoria[i]
        color_est = "green" if c[3] == "Activo" else "red"
        console.print(f"  [yellow]{i + 1}[/yellow]. ID {c[0]} - {c[1]} [{color_est}]({c[3]})[/{color_est}]")

    opciones = [str(i + 1) for i in range(len(categoria))]
    opciones.append("0")
    opc = pedir_opcion_menu("Seleccione el número de categoría a cambiar estado (0 para cancelar):", opciones)
    if opc == "0":
        return

    idx = int(opc) - 1
    c = categoria[idx]

    if c[3] == "Inactivo":
        reactivar = pedir_texto_no_vacio(f"La categoría '{c[1]}' está INACTIVA. ¿Desea reactivarla? (s/n):").lower()
        if reactivar == "s":
            c[3] = "Activo"
            mostrar_mensaje(f"Categoría '{c[1]}' reactivada con éxito.", "exito")
        else:
            mostrar_mensaje("Operación cancelada.", "info")
    else:
        confirmar = pedir_texto_no_vacio(f"¿Confirmar baja lógica de la categoría '{c[1]}'? (s/n):").lower()
        if confirmar == "s":
            c[3] = "Inactivo"
            mostrar_mensaje(f"Categoría '{c[1]}' dada de baja correctamente (Inactivo).", "exito")
        else:
            mostrar_mensaje("Operación cancelada.", "info")

    console.input("[dim]Presione ENTER para continuar...[/dim]")