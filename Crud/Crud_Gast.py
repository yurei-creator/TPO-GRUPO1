from Func.Func_Rich import console, mostrar_mensaje, renderizar_tabla
from Func.Func_val import (
    pedir_monto,
    pedir_monto_opcional,
    solicitar_y_verificar_fecha,
    solicitar_fecha_opcional,
    pedir_texto_no_vacio,
    pedir_opcional,
    pedir_opcion_menu,
    seleccionar_categoria_id,
    filtrar_por_fechas_recursivo
)
from Func.Func_Matriz import (
    obtener_nombre_categoria,
    obtener_categoria_por_id,
    obtener_presupuesto_por_categoria,
    fila_a_diccionario
)
from rich.table import Table
from rich.panel import Panel

def agregar_gasto(gastos, categorias, presupuestos):
    console.print("\n[bold green]--- [C] REGISTRAR NUEVO GASTO ---[/bold green]")
    id_cat = seleccionar_categoria_id(categorias)
    if not id_cat:
        return

    descripcion = pedir_texto_no_vacio("Ingrese concepto / descripción del gasto:")
    monto = pedir_monto("Ingrese monto del gasto:")
    fecha = solicitar_y_verificar_fecha("Fecha del gasto (DD/MM/AAAA):")

    ids_existentes = [int(g[0]) for g in gastos if g[0].isdigit()]
    nuevo_id = str(max(ids_existentes) + 1) if ids_existentes else "1"

    gastos.append([nuevo_id, fecha, monto, id_cat, descripcion, "Activo"])
    nom_cat = obtener_nombre_categoria(id_cat, categorias)
    mostrar_mensaje(f"Gasto registrado exitosamente con ID: {nuevo_id} por ${monto:,.2f} en '{nom_cat}'.", "exito")

    # Alerta de presupuesto si corresponde
    pres = obtener_presupuesto_por_categoria(id_cat, presupuestos)
    if pres:
        limite = float(pres[3])
        total_acumulado = sum([float(g[2]) for g in gastos if g[3] == id_cat and g[5] == "Activo"])
        if total_acumulado > limite:
            exceso = total_acumulado - limite
            mostrar_mensaje(f"¡ATENCIÓN! Se ha superado el presupuesto para '{nom_cat}' por ${exceso:,.2f} (Límite: ${limite:,.2f} | Consumo actual: ${total_acumulado:,.2f}).", "alerta")
        else:
            disponible = limite - total_acumulado
            console.print(f"[dim]Presupuesto restante en {nom_cat}: ${disponible:,.2f} (Límite: ${limite:,.2f})[/dim]")

    console.input("[dim]Presione ENTER para continuar...[/dim]")

def consultar_gasto(gastos, categorias, presupuestos, encabezadosG):
    console.print("\n[bold yellow]--- [R] CONSULTAR GASTO ESPECÍFICO ---[/bold yellow]")
    if not gastos:
        mostrar_mensaje("No hay gastos registrados en el sistema.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    busqueda = pedir_texto_no_vacio("Ingrese término de búsqueda (ID, descripción o categoría):").lower()
    coincidencias = []

    for g in gastos:
        nom_c = obtener_nombre_categoria(g[3], categorias).lower()
        if busqueda == g[0].lower() or busqueda in g[4].lower() or busqueda in nom_c:
            coincidencias.append(g)

    if not coincidencias:
        mostrar_mensaje("No se encontraron gastos que coincidan con la búsqueda.", "alerta")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    for g in coincidencias:
        # Conversión a diccionario con dict(zip(...)) (Clase 6)
        g_dict = fila_a_diccionario(encabezadosG, g)
        cat_info = obtener_categoria_por_id(g[3], categorias)
        nom_cat = cat_info[1] if cat_info else "Sin Categoría"
        desc_cat = cat_info[2] if cat_info else "-"

        pres_info = obtener_presupuesto_por_categoria(g[3], presupuestos)
        pres_str = f"${float(pres_info[3]):,.2f} ({pres_info[2]})" if pres_info else "Sin presupuesto asignado"

        panel_info = (
            f"[bold white]ID del Gasto:[/bold white] {g_dict['ID']}\n"
            f"[bold white]Fecha:[/bold white] {g_dict['Fecha']}\n"
            f"[bold white]Monto:[/bold white] [green]${float(g_dict['Monto']):,.2f}[/green]\n"
            f"[bold white]Descripción:[/bold white] {g_dict['Descripcion']}\n"
            f"[bold white]Estado:[/bold white] {g_dict['Estado']}\n"
            f"--------------------------------------------------\n"
            f"[bold cyan]Datos de la Categoría Asociada:[/bold cyan]\n"
            f"  • Nombre: {nom_cat} (ID {g[3]})\n"
            f"  • Detalle: {desc_cat}\n"
            f"[bold cyan]Presupuesto de la Categoría:[/bold cyan]\n"
            f"  • {pres_str}"
        )
        console.print(Panel(panel_info, title=f"[bold magenta]Gasto #{g[0]}[/bold magenta]", border_style="cyan"))

    console.input("[dim]Presione ENTER para continuar...[/dim]")

def consultar_gastos_por_rango_fechas(gastos, categorias, encabezadosG):
    console.print("\n[bold cyan]--- CONSULTA DE GASTOS POR RANGO DE FECHAS ---[/bold cyan]")
    f_inicio = solicitar_y_verificar_fecha("Ingrese fecha inicial (DD/MM/AAAA):")
    f_fin = solicitar_y_verificar_fecha("Ingrese fecha final (DD/MM/AAAA):")

    # Ejecución de la función recursiva
    resultados = filtrar_por_fechas_recursivo(gastos, f_inicio, f_fin)

    if not resultados:
        mostrar_mensaje(f"No se registraron gastos activos entre el {f_inicio} y el {f_fin}.", "alerta")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    filas = []
    total_periodo = 0.0
    for g in resultados:
        nom_cat = obtener_nombre_categoria(g[3], categorias)
        monto = float(g[2])
        total_periodo += monto
        filas.append([g[0], g[1], f"${monto:,.2f}", nom_cat, g[4]])

    encs = ["ID", "Fecha", "Monto", "Categoría", "Descripción"]
    renderizar_tabla(encs, filas, f"Gastos Registrados ({f_inicio} al {f_fin})")
    console.print(Panel(f"[bold white]Gasto Total en el Período Evaluado:[/bold white] [bold green]${total_periodo:,.2f}[/bold green]", border_style="green"))
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def modificar_gasto(gastos, categorias):
    console.print("\n[bold blue]--- [U] MODIFICAR GASTO ---[/bold blue]")
    activos = [g for g in gastos if g[5] == "Activo"]
    if not activos:
        mostrar_mensaje("No hay gastos activos para modificar.", "alerta")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    for i in range(len(activos)):
        g = activos[i]
        nom_c = obtener_nombre_categoria(g[3], categorias)
        console.print(f"  [yellow]{i + 1}[/yellow]. ID {g[0]} - {g[1]} | ${float(g[2]):,.2f} | {nom_c} - {g[4]}")

    opciones = [str(i + 1) for i in range(len(activos))]
    opciones.append("0")
    opc = pedir_opcion_menu("Seleccione el gasto a modificar (0 para cancelar):", opciones)
    if opc == "0":
        return

    idx = int(opc) - 1
    g_sel = activos[idx]

    console.print("\n[dim]Presione ENTER para conservar el dato actual:[/dim]")
    g_sel[4] = pedir_opcional("Nueva descripción", g_sel[4])
    g_sel[2] = pedir_monto_opcional("Nuevo monto", g_sel[2])
    g_sel[1] = solicitar_fecha_opcional("Nueva fecha", g_sel[1])

    cambiar_cat = pedir_texto_no_vacio("¿Desea reasignar la categoría? (s/n):").lower()
    if cambiar_cat == "s":
        nuevo_id_cat = seleccionar_categoria_id(categorias)
        if nuevo_id_cat:
            g_sel[3] = nuevo_id_cat

    cambiar_est = pedir_texto_no_vacio(f"¿Cambiar estado actual ({g_sel[5]})? (s/n):").lower()
    if cambiar_est == "s":
        g_sel[5] = "Inactivo" if g_sel[5] == "Activo" else "Activo"
        mostrar_mensaje(f"Estado modificado a: {g_sel[5]}", "info")

    mostrar_mensaje("Gasto modificado exitosamente.", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def eliminar_gasto(gastos, categorias):
    console.print("\n[bold red]--- [D] BAJA / REACTIVACIÓN LÓGICA DE GASTO ---[/bold red]")
    if not gastos:
        mostrar_mensaje("No hay gastos registrados.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    for i in range(len(gastos)):
        g = gastos[i]
        nom_c = obtener_nombre_categoria(g[3], categorias)
        col_est = "green" if g[5] == "Activo" else "red"
        console.print(f"  [yellow]{i + 1}[/yellow]. ID {g[0]} - {g[1]} | ${float(g[2]):,.2f} | {nom_c} - {g[4]} [{col_est}]({g[5]})[/{col_est}]")

    opciones = [str(i + 1) for i in range(len(gastos))]
    opciones.append("0")
    opc = pedir_opcion_menu("Seleccione el gasto a cambiar estado (0 para cancelar):", opciones)
    if opc == "0":
        return

    idx = int(opc) - 1
    g = gastos[idx]

    if g[5] == "Inactivo":
        reactivar = pedir_texto_no_vacio(f"El gasto '{g[4]}' (${float(g[2]):,.2f}) está INACTIVO. ¿Desea reactivarlo? (s/n):").lower()
        if reactivar == "s":
            g[5] = "Activo"
            mostrar_mensaje("Gasto reactivado correctamente.", "exito")
        else:
            mostrar_mensaje("Operación cancelada.", "info")
    else:
        confirmar = pedir_texto_no_vacio(f"¿Confirmar baja lógica del gasto '{g[4]}' (${float(g[2]):,.2f})? (s/n):").lower()
        if confirmar == "s":
            g[5] = "Inactivo"
            mostrar_mensaje("Gasto dado de baja correctamente (Inactivo).", "exito")
        else:
            mostrar_mensaje("Operación cancelada.", "info")

    console.input("[dim]Presione ENTER para continuar...[/dim]")