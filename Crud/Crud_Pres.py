from Func.Func_Rich import console, mostrar_mensaje, renderizar_tabla
from Func.Func_val import (
    pedir_monto,
    pedir_monto_opcional,
    solicitar_y_verificar_fecha,
    pedir_texto_no_vacio,
    pedir_opcional,
    pedir_opcion_menu,
    seleccionar_categoria_id
)
from Func.Func_Matriz import obtener_nombre_categoria, fila_a_diccionario
from rich.table import Table

def agregar_presupuesto(presupuestos, categorias):
    console.print("\n[bold green]--- [C] AGREGAR NUEVO PRESUPUESTO ---[/bold green]")
    id_cat = seleccionar_categoria_id(categorias)
    if not id_cat:
        return

    # Verificar si ya existe un presupuesto activo para esa categoría
    for p in presupuestos:
        if p[1] == id_cat and p[4] == "Activo":
            nom_c = obtener_nombre_categoria(id_cat, categorias)
            mostrar_mensaje(f"Ya existe un presupuesto activo asignado a la categoría '{nom_c}'.", "alerta")
            console.input("[dim]Presione ENTER para continuar...[/dim]")
            return

    console.print("[dim]Definición del período de vigencia:[/dim]")
    f_inicio = solicitar_y_verificar_fecha("Fecha de Inicio (DD/MM/AAAA):")
    f_fin = solicitar_y_verificar_fecha("Fecha de Cierre (DD/MM/AAAA):")
    periodo = f"{f_inicio}-{f_fin}"

    monto = pedir_monto("Ingrese monto límite mensual asignado:")
    
    ids_existentes = [int(p[0]) for p in presupuestos if p[0].isdigit()]
    nuevo_id = str(max(ids_existentes) + 1) if ids_existentes else "1"

    presupuestos.append([nuevo_id, id_cat, periodo, monto, "Activo"])
    nom_cat = obtener_nombre_categoria(id_cat, categorias)
    mostrar_mensaje(f"Presupuesto para '{nom_cat}' creado con éxito (ID: {nuevo_id}, Límite: ${monto:,.2f}).", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def consultar_presupuesto(presupuestos, categorias, gastos, encabezadosP):
    console.print("\n[bold yellow]--- [R] CONSULTAR / BUSCAR PRESUPUESTO ---[/bold yellow]")
    if not presupuestos:
        mostrar_mensaje("No hay presupuestos registrados en el sistema.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    busqueda = pedir_texto_no_vacio("Ingrese término de búsqueda (ID, Período o Nombre de Categoría):").lower()
    coincidencias = []

    for p in presupuestos:
        nom_cat = obtener_nombre_categoria(p[1], categorias).lower()
        if busqueda == p[0].lower() or busqueda in p[2].lower() or busqueda in nom_cat:
            coincidencias.append(p)

    if not coincidencias:
        mostrar_mensaje("No se encontraron presupuestos que coincidan con la búsqueda.", "alerta")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    for p in coincidencias:
        p_dict = fila_a_diccionario(encabezadosP, p)
        nom_cat = obtener_nombre_categoria(p[1], categorias)
        limite = float(p[3])

        # Buscar gastos de la categoría asociada (Entidad A -> B)
        gastos_asoc = [g for g in gastos if g[3] == p[1] and g[5] == "Activo"]
        total_gastado = sum([float(g[2]) for g in gastos_asoc])
        saldo = limite - total_gastado
        porcentaje = round((total_gastado * 100.0) / limite, 1) if limite > 0 else 0.0

        console.print(f"\n[bold cyan]Ficha de Presupuesto ID {p_dict['ID']}:[/bold cyan]")
        console.print(f"  • [bold white]Categoría Vinculada:[/bold white] {nom_cat} (ID {p[1]})")
        console.print(f"  • [bold white]Período Vigente:[/bold white] {p_dict['Periodo']}")
        console.print(f"  • [bold white]Monto Límite:[/bold white] ${limite:,.2f}")
        console.print(f"  • [bold white]Gasto Real Acumulado:[/bold white] ${total_gastado:,.2f} ({porcentaje}% consumido)")
        if saldo >= 0:
            console.print(f"  • [bold green]Saldo Restante:[/bold green] ${saldo:,.2f}")
        else:
            console.print(f"  • [bold red]EXCEDIDO EN:[/bold red] ${abs(saldo):,.2f}")
        console.print(f"  • [bold white]Estado:[/bold white] {p_dict['Estado']}")

    console.print()
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def modificar_presupuesto(presupuestos, categorias):
    console.print("\n[bold blue]--- [U] MODIFICAR PRESUPUESTO ---[/bold blue]")
    activas = [p for p in presupuestos if p[4] == "Activo"]
    if not activas:
        mostrar_mensaje("No hay presupuestos activos para modificar.", "alerta")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    console.print("Seleccione el presupuesto a modificar:")
    for i in range(len(activas)):
        p = activas[i]
        nom_c = obtener_nombre_categoria(p[1], categorias)
        console.print(f"  [yellow]{i + 1}[/yellow]. ID {p[0]} - {nom_c} | Período: {p[2]} | Límite: ${float(p[3]):,.2f}")

    opciones = [str(i + 1) for i in range(len(activas))]
    opciones.append("0")
    opc = pedir_opcion_menu("Seleccione opción (0 para cancelar):", opciones)
    if opc == "0":
        return

    idx = int(opc) - 1
    p_sel = activas[idx]

    console.print("\n[dim]Presione ENTER para conservar los valores actuales:[/dim]")
    p_sel[2] = pedir_opcional("Nuevo período (DD/MM/AAAA-DD/MM/AAAA)", p_sel[2])
    p_sel[3] = pedir_monto_opcional("Nuevo monto límite", p_sel[3])

    cambiar_cat = pedir_texto_no_vacio("¿Desea reasignar la categoría asociada? (s/n):").lower()
    if cambiar_cat == "s":
        nuevo_id_cat = seleccionar_categoria_id(categorias)
        if nuevo_id_cat:
            p_sel[1] = nuevo_id_cat

    cambiar_est = pedir_texto_no_vacio(f"¿Cambiar estado actual ({p_sel[4]})? (s/n):").lower()
    if cambiar_est == "s":
        p_sel[4] = "Inactivo" if p_sel[4] == "Activo" else "Activo"
        mostrar_mensaje(f"Estado cambiado a: {p_sel[4]}", "info")

    mostrar_mensaje("Presupuesto actualizado exitosamente.", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def eliminar_presupuesto(presupuestos, categorias):
    console.print("\n[bold red]--- [D] BAJA / REACTIVACIÓN LÓGICA DE PRESUPUESTO ---[/bold red]")
    if not presupuestos:
        mostrar_mensaje("No hay presupuestos registrados.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    for i in range(len(presupuestos)):
        p = presupuestos[i]
        nom_c = obtener_nombre_categoria(p[1], categorias)
        col_est = "green" if p[4] == "Activo" else "red"
        console.print(f"  [yellow]{i + 1}[/yellow]. ID {p[0]} - {nom_c} | Límite: ${float(p[3]):,.2f} [{col_est}]({p[4]})[/{col_est}]")

    opciones = [str(i + 1) for i in range(len(presupuestos))]
    opciones.append("0")
    opc = pedir_opcion_menu("Seleccione el presupuesto (0 para cancelar):", opciones)
    if opc == "0":
        return

    idx = int(opc) - 1
    p = presupuestos[idx]
    nom_c = obtener_nombre_categoria(p[1], categorias)

    if p[4] == "Inactivo":
        reactivar = pedir_texto_no_vacio(f"El presupuesto de '{nom_c}' está INACTIVO. ¿Desea reactivarlo? (s/n):").lower()
        if reactivar == "s":
            p[4] = "Activo"
            mostrar_mensaje("Presupuesto reactivado correctamente.", "exito")
        else:
            mostrar_mensaje("Operación cancelada.", "info")
    else:
        confirmar = pedir_texto_no_vacio(f"¿Confirmar baja lógica del presupuesto para '{nom_c}'? (s/n):").lower()
        if confirmar == "s":
            p[4] = "Inactivo"
            mostrar_mensaje("Presupuesto dado de baja correctamente (Inactivo).", "exito")
        else:
            mostrar_mensaje("Operación cancelada.", "info")

    console.input("[dim]Presione ENTER para continuar...[/dim]")
