from functools import reduce
from .Func_Rich import console, mostrar_mensaje, renderizar_tabla
from .Func_Matriz import obtener_nombre_categoria
from .Func_val import pedir_monto, pedir_opcion_menu, fecha_a_numero
from rich.panel import Panel
from rich.table import Table

def obtener_gastos_activos(gastos):
    return list(filter(lambda g: g[5] == "Activo", gastos))

def calcular_total_gastos(gastos):
    activos = obtener_gastos_activos(gastos)
    if not activos:
        return 0.0
    return reduce(lambda acc, g: acc + float(g[2]), activos, 0.0)

def calcular_promedio_general(gastos):
    activos = obtener_gastos_activos(gastos)
    if not activos:
        return 0.0
    total = calcular_total_gastos(gastos)
    return total / len(activos)

def calcular_estadisticas_por_categoria(gastos, categorias):
    activos = obtener_gastos_activos(gastos)
    total_general = calcular_total_gastos(gastos)
    resumen = []

    for c in categorias:
        id_cat = c[0]
        nom_cat = c[1]
        gastos_cat = list(filter(lambda g: g[3] == id_cat, activos))
        conteo = len(gastos_cat)
        
        if conteo > 0:
            subtotal = reduce(lambda acc, g: acc + float(g[2]), gastos_cat, 0.0)
            promedio = subtotal / conteo
            porcentaje = (lambda sub, tot: round((sub * 100.0) / tot, 2) if tot > 0 else 0.0)(subtotal, total_general)
        else:
            subtotal = 0.0
            promedio = 0.0
            porcentaje = 0.0

        resumen.append({
            "id_cat": id_cat,
            "nombre": nom_cat,
            "conteo": conteo,
            "subtotal": subtotal,
            "promedio": promedio,
            "porcentaje": porcentaje
        })

    return resumen

def obtener_maximo_y_minimo(gastos, categorias):
    activos = obtener_gastos_activos(gastos)
    if not activos:
        return None, None
    ordenados = sorted(activos, key=lambda g: float(g[2]))
    return ordenados[0], ordenados[-1]

def mostrar_promedios(gastos, categorias):
    console.print("\n[bold cyan]--- REPORTE DE PROMEDIOS ---[/bold cyan]")
    activos = obtener_gastos_activos(gastos)
    if not activos:
        mostrar_mensaje("No hay gastos activos para calcular promedios.", "alerta")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    prom_gen = calcular_promedio_general(gastos)
    total_gen = calcular_total_gastos(gastos)
    
    console.print(Panel(
        f"[bold white]Gasto Total Acumulado:[/bold white] [green]${total_gen:,.2f}[/green]\n"
        f"[bold white]Promedio General por Gasto:[/bold white] [yellow]${prom_gen:,.2f}[/yellow]",
        title="[bold magenta]Promedio General[/bold magenta]",
        border_style="cyan"
    ))

    datos_cat = calcular_estadisticas_por_categoria(gastos, categorias)
    encabezados = ["Categoría", "Cantidad de Gastos", "Gasto Subtotal", "Promedio por Registro"]
    filas = []
    for d in datos_cat:
        filas.append([
            d["nombre"],
            str(d["conteo"]),
            f"${d['subtotal']:,.2f}",
            f"${d['promedio']:,.2f}"
        ])

    renderizar_tabla(encabezados, filas, "Promedios por Categoría")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def mostrar_conteos(gastos, categorias):
    console.print("\n[bold cyan]--- CONTEO DE REGISTROS ---[/bold cyan]")
    activos = obtener_gastos_activos(gastos)
    total_registros = len(activos)
    
    datos_cat = calcular_estadisticas_por_categoria(gastos, categorias)
    encabezados = ["ID", "Categoría", "Cantidad de Registros Activos"]
    filas = []
    for d in datos_cat:
        filas.append([d["id_cat"], d["nombre"], str(d["conteo"])])

    console.print(Panel(
        f"[bold white]Total de Gastos Activos Registrados:[/bold white] [green]{total_registros}[/green]",
        title="[bold magenta]Conteo General[/bold magenta]",
        border_style="magenta"
    ))
    renderizar_tabla(encabezados, filas, "Distribución de Gastos por Categoría")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def mostrar_porcentajes_relativos(gastos, categorias):
    console.print("\n[bold cyan]--- PORCENTAJES RELATIVOS POR CATEGORÍA ---[/bold cyan]")
    activos = obtener_gastos_activos(gastos)
    if not activos:
        mostrar_mensaje("No hay gastos registrados para calcular porcentajes.", "alerta")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    total_general = calcular_total_gastos(gastos)
    datos_cat = calcular_estadisticas_por_categoria(gastos, categorias)

    # Uso explícito de map con lambda sobre la colección
    porcentajes_mapeados = list(map(
        lambda d: [d["nombre"], f"${d['subtotal']:,.2f}", f"{d['porcentaje']}%"],
        datos_cat
    ))

    encabezados = ["Categoría", "Monto Invertido", "Porcentaje sobre el Total"]
    renderizar_tabla(encabezados, porcentajes_mapeados, "Participación Porcentual de Gastos")
    console.print(f"[dim]Total general de referencia: ${total_general:,.2f}[/dim]\n")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def mostrar_maximos_y_minimos(gastos, categorias):
    console.print("\n[bold cyan]--- IDENTIFICACIÓN DE VALORES MÁXIMOS Y MÍNIMOS ---[/bold cyan]")
    g_min, g_max = obtener_maximo_y_minimo(gastos, categorias)

    if not g_min or not g_max:
        mostrar_mensaje("No hay suficientes registros para comparar valores.", "alerta")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    cat_min = obtener_nombre_categoria(g_min[3], categorias)
    cat_max = obtener_nombre_categoria(g_max[3], categorias)

    tabla = Table(title="[bold cyan]Extremos de Gastos Registrados[/bold cyan]", header_style="bold magenta", border_style="bright_blue")
    tabla.add_column("Criterio", style="bold yellow")
    tabla.add_column("ID", justify="center")
    tabla.add_column("Fecha", justify="center")
    tabla.add_column("Monto", justify="right", style="bold green")
    tabla.add_column("Categoría", style="cyan")
    tabla.add_column("Descripción", style="white")

    tabla.add_row(
        "Gasto Mínimo",
        g_min[0],
        g_min[1],
        f"${float(g_min[2]):,.2f}",
        cat_min,
        g_min[4]
    )
    tabla.add_row(
        "Gasto Máximo",
        g_max[0],
        g_max[1],
        f"${float(g_max[2]):,.2f}",
        cat_max,
        g_max[4]
    )

    console.print()
    console.print(tabla)
    console.print()
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def ordenar_gastos_interactivo(gastos, categorias):
    console.print("\n[bold cyan]--- ORDENAMIENTO DINÁMICO DE GASTOS ---[/bold cyan]")
    activos = obtener_gastos_activos(gastos)
    if not activos:
        mostrar_mensaje("No hay gastos activos para ordenar.", "alerta")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    console.print("1. Ordenar por Monto")
    console.print("2. Ordenar por Fecha")
    console.print("3. Ordenar por Descripción")
    criterio = pedir_opcion_menu("Seleccione criterio (1/2/3):", ["1", "2", "3"])

    console.print("\n1. De menor a mayor (Ascendente)")
    console.print("2. De mayor a menor (Descendente)")
    sentido = pedir_opcion_menu("Seleccione orden (1/2):", ["1", "2"])
    es_descendente = (sentido == "2")

    if criterio == "1":
        gastos_ordenados = sorted(activos, key=lambda g: float(g[2]), reverse=es_descendente)
        titulo = "Gastos Ordenados por Monto"
    elif criterio == "2":
        gastos_ordenados = sorted(activos, key=lambda g: fecha_a_numero(g[1]), reverse=es_descendente)
        titulo = "Gastos Ordenados por Fecha"
    else:
        gastos_ordenados = sorted(activos, key=lambda g: g[4].lower(), reverse=es_descendente)
        titulo = "Gastos Ordenados por Descripción"

    encabezados = ["ID", "Fecha", "Monto", "Categoría", "Descripción"]
    filas = []
    for g in gastos_ordenados:
        nom_cat = obtener_nombre_categoria(g[3], categorias)
        filas.append([g[0], g[1], f"${float(g[2]):,.2f}", nom_cat, g[4]])

    renderizar_tabla(encabezados, filas, titulo)
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def comparativa_gastos_vs_presupuestos(gastos, categorias, presupuestos):
    console.print("\n[bold cyan]--- COMPARATIVA DE GASTOS VS. PRESUPUESTOS ---[/bold cyan]")
    datos_cat = calcular_estadisticas_por_categoria(gastos, categorias)
    
    encabezados = ["Categoría", "Presupuesto Límite", "Gasto Real", "Diferencia / Saldo", "Consumo (%)", "Estado"]
    filas = []

    for d in datos_cat:
        id_c = d["id_cat"]
        gasto_real = d["subtotal"]
        
        pres = None
        for p in presupuestos:
            if p[1] == id_c and p[4] == "Activo":
                pres = p
                break

        if pres:
            limite = float(pres[3])
            saldo = limite - gasto_real
            porc_consumo = round((gasto_real * 100.0) / limite, 1) if limite > 0 else 0.0
            
            if saldo >= 0:
                estado_alerta = "[green]Dentro de Presupuesto[/green]"
                saldo_str = f"+${saldo:,.2f}"
            else:
                estado_alerta = "[bold red]EXCEDIDO[/bold red]"
                saldo_str = f"-${abs(saldo):,.2f}"

            filas.append([
                d["nombre"],
                f"${limite:,.2f}",
                f"${gasto_real:,.2f}",
                saldo_str,
                f"{porc_consumo}%",
                estado_alerta
            ])
        else:
            filas.append([
                d["nombre"],
                "Sin Presupuesto",
                f"${gasto_real:,.2f}",
                "-",
                "-",
                "[dim]No Asignado[/dim]"
            ])

    renderizar_tabla(encabezados, filas, "Gasto Real vs. Presupuesto Previsto")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def simulacion_proyeccion_inflacion(gastos):
    console.print("\n[bold cyan]--- ESTIMACIÓN DE VARIACIÓN / PROYECCIÓN DE GASTOS ---[/bold cyan]")
    activos = obtener_gastos_activos(gastos)
    if not activos:
        mostrar_mensaje("No hay gastos activos para realizar la proyección.", "alerta")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    total_actual = calcular_total_gastos(gastos)
    console.print(f"Gasto actual total mensual de referencia: [bold green]${total_actual:,.2f}[/bold green]\n")

    console.print("1. Proyección Mensual")
    console.print("2. Proyección Anual")
    modo = pedir_opcion_menu("Seleccione modalidad (1/2):", ["1", "2"])

    tiempo = pedir_monto("Ingrese la cantidad de períodos (meses o años):")
    tasa_input = pedir_monto("Ingrese la tasa de variación estimada (%):")

    periodos = tiempo if modo == "1" else tiempo * 12
    tasa_decimal = (tasa_input / 100.0) if modo == "1" else (tasa_input / 100.0) / 12

    # Cálculo acumulado utilizando expresión lambda (del módulo pruebasLambda)
    factor_acumulado = (lambda a, b, c: ((a + b) ** c) - a)(1.0, tasa_decimal, periodos)
    gasto_proyectado = (lambda base, factor: base + (base * factor))(total_actual, factor_acumulado)
    diferencia = gasto_proyectado - total_actual

    console.print(Panel(
        f"[bold white]Gasto Base Actual:[/bold white] ${total_actual:,.2f}\n"
        f"[bold white]Períodos evaluados:[/bold white] {int(periodos)} meses\n"
        f"[bold white]Variación acumulada proyectada:[/bold white] +${diferencia:,.2f} ({factor_acumulado * 100:.2f}%)\n"
        f"[bold yellow]Gasto Futuro Estimado:[/bold yellow] [bold green]${gasto_proyectado:,.2f}[/bold green]",
        title="[bold cyan]Resultado de Proyección[/bold cyan]",
        border_style="green"
    ))
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def mostrar_resumen_estadistico_completo(gastos, categorias, presupuestos):
    console.print("\n[bold cyan]===========================================================[/bold cyan]")
    console.print("[bold cyan]             RESUMEN ESTADÍSTICO GENERAL                  [/bold cyan]")
    console.print("[bold cyan]===========================================================[/bold cyan]")

    activos = obtener_gastos_activos(gastos)
    if not activos:
        mostrar_mensaje("No hay gastos registrados en el sistema.", "alerta")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    total = calcular_total_gastos(gastos)
    promedio = calcular_promedio_general(gastos)
    g_min, g_max = obtener_maximo_y_minimo(gastos, categorias)

    panel_resumen = (
        f"[bold white]• Total de Gastos Registrados:[/bold white] [cyan]{len(activos)}[/cyan]\n"
        f"[bold white]• Sumatoria Total Acumulada:[/bold white] [green]${total:,.2f}[/green]\n"
        f"[bold white]• Promedio General por Gasto:[/bold white] [yellow]${promedio:,.2f}[/yellow]\n"
        f"[bold white]• Gasto Mínimo:[/bold white] [blue]${float(g_min[2]):,.2f}[/blue] ({obtener_nombre_categoria(g_min[3], categorias)} - {g_min[4]})\n"
        f"[bold white]• Gasto Máximo:[/bold white] [red]${float(g_max[2]):,.2f}[/red] ({obtener_nombre_categoria(g_max[3], categorias)} - {g_max[4]})"
    )
    console.print(Panel(panel_resumen, title="[bold yellow]Métricas Clave[/bold yellow]", border_style="yellow"))

    # Desglose por categoría
    comparativa_gastos_vs_presupuestos(gastos, categorias, presupuestos)
