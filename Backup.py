# =============================================================================
# SISTEMA DE CONTROL DE GASTOS PERSONALES Y FAMILIARES (VERSION MONOLITICA BACKUP)
# Programación 1 - Algoritmos y Estructuras de Datos 1
# Código completo consolidado en un solo archivo sin dependencias modulares relativas.
# =============================================================================

import re
from functools import reduce
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# =============================================================================
# 1. DATOS INICIALES DEL SISTEMA
# =============================================================================

encabezadosC = ["ID", "Nombre", "Descripcion", "Estado"]
encabezadosP = ["ID", "ID_Categoria", "Periodo", "Monto Limite", "Estado"]
encabezadosG = ["ID", "Fecha", "Monto", "ID_Categoria", "Descripcion", "Estado"]

categoria = [
    ["1", "Alimentos", "Gastos de supermercado, carnicería y verdulería", "Activo"],
    ["2", "Transporte", "Combustible, pasajes y mantenimiento vehicular", "Activo"],
    ["3", "Ocio", "Salidas, cine, restaurantes y recreación", "Activo"],
    ["4", "Salud", "Farmacia, consultas médicas y medicamentos", "Activo"],
    ["5", "Educación", "Cursos, libros y materiales de estudio", "Activo"],
]

presupuestos = [
    ["1", "1", "01/08/2026-31/08/2026", 50000.0, "Activo"],
    ["2", "2", "01/08/2026-31/08/2026", 20000.0, "Activo"],
    ["3", "3", "01/08/2026-31/08/2026", 15000.0, "Activo"],
    ["4", "4", "01/08/2026-31/08/2026", 10000.0, "Activo"],
    ["5", "5", "01/08/2026-31/08/2026", 12000.0, "Activo"],
]

gastos = [
    ["1", "01/08/2026", 12500.0, "1", "Supermercado compra semanal", "Activo"],
    ["2", "02/08/2026", 4500.0, "2", "Carga de combustible", "Activo"],
    ["3", "03/08/2026", 3200.0, "3", "Entradas de cine y combo", "Activo"],
    ["4", "04/08/2026", 1800.0, "4", "Farmacia medicamentos", "Activo"],
    ["5", "05/08/2026", 7500.0, "5", "Pago cuota curso online", "Activo"],
    ["6", "10/08/2026", 18200.0, "1", "Compra mensual supermercado", "Activo"],
    ["7", "12/08/2026", 6000.0, "2", "Recarga de tarjeta transporte", "Activo"],
    ["8", "15/08/2026", 5400.0, "3", "Cena con amigos", "Activo"],
]

PERMISOS_DISPONIBLES = ["gastos", "categorias", "presupuestos", "reportes", "usuarios"]

roles_permisos = {
    "administrador": {"gastos", "categorias", "presupuestos", "reportes", "usuarios"},
    "editor": {"gastos", "categorias", "presupuestos", "reportes"},
    "lector": {"reportes"}
}

usuarios = [
    {
        "id": 1,
        "user": "admin",
        "pass": "Admin1234",
        "rol": "administrador",
        "permisos": {"gastos", "categorias", "presupuestos", "reportes", "usuarios"},
        "estado": "Activo"
    },
    {
        "id": 2,
        "user": "familiar",
        "pass": "Familiar2026",
        "rol": "editor",
        "permisos": {"gastos", "categorias", "presupuestos", "reportes"},
        "estado": "Activo"
    },
    {
        "id": 3,
        "user": "invitado",
        "pass": "User1234",
        "rol": "lector",
        "permisos": {"reportes"},
        "estado": "Activo"
    }
]

# =============================================================================
# 2. FUNCIONES DE INTERFAZ RICH
# =============================================================================

def mostrar_mensaje(texto, tipo="info"):
    estilos = {
        "info": ("cyan", "INFORMACIÓN"),
        "exito": ("green", "ÉXITO"),
        "alerta": ("yellow", "ADVERTENCIA"),
        "error": ("red", "ERROR"),
    }
    color, titulo = estilos.get(tipo, ("white", "MENSAJE"))
    panel = Panel(
        f"[{color}]{texto}[/{color}]",
        title=f"[bold {color}]{titulo}[/bold {color}]",
        border_style=color,
        expand=False,
    )
    console.print(panel)

def renderizar_tabla(encabezados, filas, titulo):
    if not filas:
        console.print(f"[yellow]No hay registros para mostrar en {titulo.lower()}.[/yellow]")
        return

    tabla = Table(
        title=f"[bold cyan]{titulo}[/bold cyan]",
        header_style="bold magenta",
        border_style="bright_blue",
    )

    for enc in encabezados:
        tabla.add_column(enc, justify="left", style="white")

    for fila in filas:
        tabla.add_row(*[str(x) for x in fila])

    console.print()
    console.print(tabla)
    console.print()

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

    tabla_menu.add_row("0", "Volver al menú anterior / Salir")

    console.print()
    console.print(tabla_menu)
    console.print()

# =============================================================================
# 3. FUNCIONES DE VALIDACIÓN Y MANIPULACIÓN DE CADENAS
# =============================================================================

def pedir_monto(mensaje):
    while True:
        entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] ").strip()
        if len(entrada) == 0:
            mostrar_mensaje("El campo no puede estar vacío.", "error")
            continue
        
        entrada_norm = entrada.replace(",", ".")
        partes = entrada_norm.split(".")
        
        es_valido = False
        if len(partes) == 1 and partes[0].isdigit():
            es_valido = True
        elif len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit():
            es_valido = True

        if es_valido:
            valor = float(entrada_norm)
            if valor > 0:
                return valor
            else:
                mostrar_mensaje("El monto debe ser un número mayor a cero.", "alerta")
        else:
            mostrar_mensaje("El formato ingresado no es un número válido.", "error")

def pedir_monto_opcional(mensaje, valor_actual):
    while True:
        entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] [yellow][${valor_actual}][/yellow]: ").strip()
        if len(entrada) == 0:
            return float(valor_actual)
        
        entrada_norm = entrada.replace(",", ".")
        partes = entrada_norm.split(".")
        
        es_valido = False
        if len(partes) == 1 and partes[0].isdigit():
            es_valido = True
        elif len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit():
            es_valido = True

        if es_valido:
            valor = float(entrada_norm)
            if valor > 0:
                return valor
            else:
                mostrar_mensaje("El monto debe ser mayor a cero.", "alerta")
        else:
            mostrar_mensaje("El formato ingresado no es un número válido.", "error")

def es_fecha_valida(fecha_str):
    patron = r"^\d{2}/\d{2}/\d{4}$"
    if not re.match(patron, fecha_str):
        return False
    
    partes = fecha_str.split("/")
    dia = int(partes[0])
    mes = int(partes[1])
    anio = int(partes[2])
    
    if anio < 1900 or anio > 2100 or mes < 1 or mes > 12:
        return False
        
    es_bisiesto = (anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0))
    dias_por_mes = [31, 29 if es_bisiesto else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    if dia < 1 or dia > dias_por_mes[mes - 1]:
        return False
        
    return True

def solicitar_y_verificar_fecha(mensaje="Ingrese fecha (DD/MM/AAAA):"):
    while True:
        entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] ").strip()
        if es_fecha_valida(entrada):
            return entrada
        mostrar_mensaje("Fecha inválida en el calendario. Use el formato DD/MM/AAAA.", "error")

def solicitar_fecha_opcional(mensaje, fecha_actual):
    while True:
        entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] [yellow][{fecha_actual}][/yellow]: ").strip()
        if len(entrada) == 0:
            return fecha_actual
        if es_fecha_valida(entrada):
            return entrada
        mostrar_mensaje("Fecha inválida en el calendario. Use el formato DD/MM/AAAA.", "error")

def pedir_texto_no_vacio(mensaje):
    while True:
        entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] ").strip()
        if len(entrada) > 0:
            return entrada
        mostrar_mensaje("Este campo no puede estar vacío.", "error")

def pedir_opcional(mensaje, valor_actual):
    entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] [yellow][{valor_actual}][/yellow]: ").strip()
    if len(entrada) > 0:
        return entrada
    return valor_actual

def pedir_opcion_menu(mensaje, opciones_validas):
    patron = r"^[0-9]+$"
    while True:
        entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] ").strip()
        if re.match(patron, entrada) and entrada in opciones_validas:
            return entrada
        mostrar_mensaje("Opción inválida. Seleccione una de las opciones numéricas disponibles.", "error")

def seleccionar_categoria_id(categorias):
    console.print("\n[bold cyan]Seleccione una Categoría:[/bold cyan]")
    activas = [c for c in categorias if c[3] == "Activo"]
    
    if not activas:
        mostrar_mensaje("No hay categorías activas registradas.", "error")
        return None

    for i in range(len(activas)):
        c = activas[i]
        console.print(f"  [yellow]{i + 1}[/yellow]. {c[1]} [dim]({c[2]})[/dim]")

    opciones = [str(i + 1) for i in range(len(activas))]
    opc = pedir_opcion_menu("Número de categoría seleccionada:", opciones)
    idx_seleccionada = int(opc) - 1
    return activas[idx_seleccionada][0]

def fecha_a_numero(fecha_str):
    partes = fecha_str.split("/")
    return int(f"{partes[2]}{partes[1]}{partes[0]}")

def filtrar_por_fechas_recursivo(gastos_lista, fecha_inicio, fecha_fin):
    if not gastos_lista:
        return []

    gasto_actual = gastos_lista[0]
    resto = filtrar_por_fechas_recursivo(gastos_lista[1:], fecha_inicio, fecha_fin)

    if gasto_actual[5] == "Activo":
        num_gasto = fecha_a_numero(gasto_actual[1])
        num_inicio = fecha_a_numero(fecha_inicio)
        num_fin = fecha_a_numero(fecha_fin)
        if num_inicio <= num_gasto <= num_fin:
            return [gasto_actual] + resto

    return resto

# =============================================================================
# 4. MANIPULACIÓN DE MATRICES Y DICCIONARIOS
# =============================================================================

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

# =============================================================================
# 5. MÓDULO DE REPORTES Y ESTADÍSTICAS (LAMBDA, MAP, FILTER, REDUCE)
# =============================================================================

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

    tabla.add_row("Gasto Mínimo", g_min[0], g_min[1], f"${float(g_min[2]):,.2f}", cat_min, g_min[4])
    tabla.add_row("Gasto Máximo", g_max[0], g_max[1], f"${float(g_max[2]):,.2f}", cat_max, g_max[4])

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

    comparativa_gastos_vs_presupuestos(gastos, categorias, presupuestos)

# =============================================================================
# 6. CRUD DE CATEGORÍAS
# =============================================================================

def agregar_categoria(categoria):
    console.print("\n[bold green]--- [C] AGREGAR NUEVA CATEGORÍA ---[/bold green]")
    ids_existentes = [int(c[0]) for c in categoria if c[0].isdigit()]
    nuevo_id = str(max(ids_existentes) + 1) if ids_existentes else "1"

    nombre = pedir_texto_no_vacio("Ingrese nombre de la categoría:")
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
        cat_dict = fila_a_diccionario(encabezadosC, c)
        
        console.print(f"\n[bold cyan]Ficha de la Categoría ID {cat_dict['ID']}:[/bold cyan]")
        console.print(f"  • [bold white]Nombre:[/bold white] {cat_dict['Nombre']}")
        console.print(f"  • [bold white]Descripción:[/bold white] {cat_dict['Descripcion']}")
        console.print(f"  • [bold white]Estado:[/bold white] {cat_dict['Estado']}")

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

# =============================================================================
# 7. CRUD DE PRESUPUESTOS
# =============================================================================

def agregar_presupuesto(presupuestos, categorias):
    console.print("\n[bold green]--- [C] AGREGAR NUEVO PRESUPUESTO ---[/bold green]")
    id_cat = seleccionar_categoria_id(categorias)
    if not id_cat:
        return

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

# =============================================================================
# 8. CRUD DE GASTOS
# =============================================================================

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

# =============================================================================
# 9. ADMINISTRACIÓN DE USUARIOS, ROLES Y LOGIN
# =============================================================================

def validar_password(password):
    if len(password) < 6:
        return False
    tiene_mayuscula = re.search(r"[A-Z]", password)
    tiene_numero = re.search(r"[0-9]", password)
    if tiene_mayuscula and tiene_numero:
        return True
    return False

def listar_usuarios():
    tabla = Table(title="[bold cyan]Listado de Usuarios Registrados[/bold cyan]", header_style="bold magenta", border_style="bright_blue")
    tabla.add_column("ID", justify="center", style="bold yellow")
    tabla.add_column("Usuario", justify="left", style="white")
    tabla.add_column("Rol", justify="left", style="cyan")
    tabla.add_column("Permisos Asignados", justify="left", style="green")
    tabla.add_column("Estado", justify="center")

    for u in usuarios:
        permisos_texto = ", ".join(sorted(list(u["permisos"])))
        est = u.get("estado", "Activo")
        color_est = "green" if est == "Activo" else "red"
        tabla.add_row(str(u["id"]), u["user"], u["rol"], permisos_texto, f"[{color_est}]{est}[/{color_est}]")

    console.print()
    console.print(tabla)
    console.print()

def registrar_usuario():
    console.print("\n[bold green]--- REGISTRO DE NUEVO USUARIO ---[/bold green]")
    nuevo_id = usuarios[-1]["id"] + 1 if len(usuarios) > 0 else 1
    
    username = console.input("[bold cyan]Ingrese nombre de usuario:[/bold cyan] ").strip()
    if [u for u in usuarios if u["user"] == username]:
        mostrar_mensaje("El nombre de usuario ingresado ya existe.", "error")
        return

    password = console.input("[bold cyan]Ingrese contraseña (mínimo 6 caracteres, 1 mayúscula y números):[/bold cyan] ").strip()
    while not validar_password(password):
        mostrar_mensaje("La contraseña no cumple con los requisitos mínimos de seguridad.", "alerta")
        password = console.input("[bold cyan]Ingrese una contraseña válida:[/bold cyan] ").strip()

    console.print("\n[dim]Roles disponibles: 1. Administrador | 2. Editor | 3. Lector[/dim]")
    opc = console.input("[bold cyan]Seleccione el rol (1/2/3):[/bold cyan] ").strip()
    
    if opc == "1":
        rol = "administrador"
        permisos = roles_permisos["administrador"].copy()
    elif opc == "2":
        rol = "editor"
        permisos = roles_permisos["editor"].copy()
    else:
        rol = "lector"
        permisos = roles_permisos["lector"].copy()

    nuevo = {
        "id": nuevo_id,
        "user": username,
        "pass": password,
        "rol": rol,
        "permisos": permisos,
        "estado": "Activo"
    }
    usuarios.append(nuevo)
    mostrar_mensaje(f"Usuario '{username}' registrado exitosamente con ID {nuevo_id}.", "exito")

def eliminar_usuario(usuario_actual=None):
    console.print("\n[bold red]--- BAJA / REACTIVACIÓN LÓGICA DE USUARIO ---[/bold red]")
    if not usuarios:
        mostrar_mensaje("No hay usuarios registrados.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    listar_usuarios()
    id_ingresado = console.input("[bold cyan]Ingrese el ID del usuario a modificar estado (0 para cancelar):[/bold cyan] ").strip()
    if id_ingresado == "0":
        return
    if not id_ingresado.isdigit():
        mostrar_mensaje("El ID ingresado debe ser un valor numérico.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    id_buscar = int(id_ingresado)
    user_sel = None
    for u in usuarios:
        if u["id"] == id_buscar:
            user_sel = u
            break

    if not user_sel:
        mostrar_mensaje("No se encontró ningún usuario con el ID especificado.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    if user_sel["user"] == "admin":
        mostrar_mensaje("No está permitido dar de baja al administrador principal del sistema.", "alerta")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    if usuario_actual and user_sel["user"] == usuario_actual.get("user"):
        mostrar_mensaje("No puedes darte de baja a ti mismo mientras tu sesión esté activa.", "alerta")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    estado_actual = user_sel.get("estado", "Activo")
    if estado_actual == "Inactivo":
        reactivar = console.input(f"[bold cyan]El usuario '{user_sel['user']}' está INACTIVO. ¿Desea reactivarlo? (s/n):[/bold cyan] ").strip().lower()
        if reactivar == "s":
            user_sel["estado"] = "Activo"
            mostrar_mensaje(f"Usuario '{user_sel['user']}' reactivado exitosamente.", "exito")
        else:
            mostrar_mensaje("Operación cancelada.", "info")
    else:
        confirmar = console.input(f"[bold cyan]¿Está seguro de dar de baja al usuario '{user_sel['user']}'? (s/n):[/bold cyan] ").strip().lower()
        if confirmar == "s":
            user_sel["estado"] = "Inactivo"
            mostrar_mensaje(f"Usuario '{user_sel['user']}' dado de baja correctamente (Inactivo).", "exito")
        else:
            mostrar_mensaje("Operación cancelada.", "info")

    console.input("[dim]Presione ENTER para continuar...[/dim]")

def verificar_permiso(usuario, permiso_requerido):
    if not usuario or "permisos" not in usuario:
        return False
    permiso_a_revisar = {permiso_requerido}
    return permiso_a_revisar.issubset(usuario["permisos"])

def mostrar_permisos_disponibles():
    tabla_permisos = Table(title="[bold yellow]Permisos Disponibles del Sistema[/bold yellow]", border_style="yellow")
    tabla_permisos.add_column("Módulo", justify="left", style="white")
    tabla_permisos.add_column("Descripción de Acceso", justify="left", style="dim")
    
    tabla_permisos.add_row("gastos", "Acceso completo a la gestión de gastos")
    tabla_permisos.add_row("categorias", "Acceso completo a la gestión de categorías")
    tabla_permisos.add_row("presupuestos", "Acceso completo a la gestión de presupuestos")
    tabla_permisos.add_row("reportes", "Acceso a reportes, tablas generales y estadísticas")
    tabla_permisos.add_row("usuarios", "Administración de cuentas y permisos de acceso")
    
    console.print(tabla_permisos)

def modificar_permisos():
    console.print("\n[bold blue]--- ADMINISTRACIÓN DE PERMISOS ---[/bold blue]")
    console.print("1. Modificar permisos de un usuario específico")
    console.print("2. Modificar permisos globales de un rol")
    tipo = console.input("[bold cyan]Seleccione una opción (1/2):[/bold cyan] ").strip()

    if tipo == "1":
        listar_usuarios()
        id_ingresado = console.input("[bold cyan]Ingrese el ID del usuario a modificar:[/bold cyan] ").strip()
        if not id_ingresado.isdigit():
            mostrar_mensaje("El ID ingresado debe ser un valor numérico.", "error")
            return
        id_buscar = int(id_ingresado)

        usuario_encontrado = None
        for u in usuarios:
            if u["id"] == id_buscar:
                usuario_encontrado = u
                break

        if not usuario_encontrado:
            mostrar_mensaje("No se encontró ningún usuario con el ID especificado.", "error")
            return

        permisos_actuales = ", ".join(sorted(list(usuario_encontrado["permisos"])))
        console.print(f"\n[bold]Usuario:[/bold] [yellow]{usuario_encontrado['user']}[/yellow]")
        console.print(f"[bold]Permisos actuales:[/bold] [green]{permisos_actuales}[/green]\n")
        
        mostrar_permisos_disponibles()

        console.print("\n[dim]Acciones: 1. Agregar permisos | 2. Quitar permisos[/dim]")
        accion = console.input("[bold cyan]Seleccione acción (1/2):[/bold cyan] ").strip()

        entrada_permisos = console.input("[bold cyan]Ingrese los permisos separados por espacio:[/bold cyan] ").strip().lower()
        nuevos_permisos = set(entrada_permisos.split())

        if accion == "1":
            usuario_encontrado["permisos"] = usuario_encontrado["permisos"] | nuevos_permisos
            mostrar_mensaje("Permisos agregados exitosamente al usuario.", "exito")
        elif accion == "2":
            usuario_encontrado["permisos"] = usuario_encontrado["permisos"] - nuevos_permisos
            mostrar_mensaje("Permisos revocados exitosamente del usuario.", "exito")
        else:
            mostrar_mensaje("Opción de acción no válida.", "error")

    elif tipo == "2":
        console.print("\n[dim]Roles configurables: administrador | editor | lector[/dim]")
        rol = console.input("[bold cyan]Ingrese el nombre del rol a configurar:[/bold cyan] ").strip().lower()

        if rol not in roles_permisos:
            mostrar_mensaje("El rol ingresado no existe en el sistema.", "error")
            return

        permisos_rol = ", ".join(sorted(list(roles_permisos[rol])))
        console.print(f"\n[bold]Rol seleccionado:[/bold] [yellow]{rol}[/yellow]")
        console.print(f"[bold]Permisos actuales del rol:[/bold] [green]{permisos_rol}[/green]\n")
        
        mostrar_permisos_disponibles()

        console.print("\n[dim]Acciones: 1. Agregar permisos | 2. Quitar permisos[/dim]")
        accion = console.input("[bold cyan]Seleccione acción (1/2):[/bold cyan] ").strip()

        entrada_permisos = console.input("[bold cyan]Ingrese los permisos separados por espacio:[/bold cyan] ").strip().lower()
        set_cambios = set(entrada_permisos.split())

        if accion == "1":
            roles_permisos[rol] = roles_permisos[rol] | set_cambios
            mostrar_mensaje(f"Permisos agregados correctamente al rol '{rol}'.", "exito")
        elif accion == "2":
            roles_permisos[rol] = roles_permisos[rol] - set_cambios
            mostrar_mensaje(f"Permisos revocados correctamente del rol '{rol}'.", "exito")
        else:
            mostrar_mensaje("Opción no válida.", "error")
            return

        actualizar = console.input("\n[bold cyan]¿Desea sincronizar estos permisos en los usuarios existentes con este rol? (s/n):[/bold cyan] ").strip().lower()
        if actualizar == "s":
            for u in usuarios:
                if u["rol"] == rol:
                    u["permisos"] = roles_permisos[rol].copy()
            mostrar_mensaje("Todos los usuarios con dicho rol fueron actualizados.", "info")

    else:
        mostrar_mensaje("Opción no válida seleccionada.", "error")

def login():
    console.print("\n[bold cyan]====================================================[/bold cyan]")
    console.print("[bold cyan]       ACCESO AL SISTEMA DE GESTION DE GASTOS      [/bold cyan]")
    console.print("[bold cyan]====================================================[/bold cyan]")
    intentos = 0
    max_intentos = 3
    
    while intentos < max_intentos:
        user = console.input("[bold]Usuario:[/bold] ").strip()
        clave = console.input("[bold]Contraseña:[/bold] ").strip()
        
        for u in usuarios:
            if u["user"] == user and u["pass"] == clave:
                if u.get("estado", "Activo") == "Inactivo":
                    mostrar_mensaje("El usuario se encuentra inactivo. Contacte al administrador.", "error")
                    return None
                mostrar_mensaje(f"Bienvenido, {u['user']}. Sesión iniciada como {u['rol'].capitalize()}.", "exito")
                return u
        
        intentos += 1
        restantes = max_intentos - intentos
        if restantes > 0:
            mostrar_mensaje(f"Credenciales incorrectas. Intentos restantes: {restantes}.", "alerta")
    
    mostrar_mensaje("Acceso bloqueado por alcanzar el límite máximo de intentos fallidos.", "error")
    return None

# =============================================================================
# 10. MENÚS Y SUBMENÚS
# =============================================================================

def menu_categorias(categoria, gastos, presupuestos, encabezadosC, encabezadosG):
    activo = True
    opciones = [
        "Mostrar todas las categorías",
        "Consultar / Buscar categoría",
        "Agregar categoría",
        "Modificar categoría",
        "Baja / Reactivación lógica de categoría",
    ]
    while activo:
        mostrar_menu("GESTIÓN DE CATEGORÍAS", opciones)
        opc = pedir_opcion_menu("Seleccione una opción:", ["0", "1", "2", "3", "4", "5"])

        if opc == "1":
            mostrar_categorias(categoria, encabezadosC)
        elif opc == "2":
            consultar_categoria(categoria, gastos, presupuestos, encabezadosC, encabezadosG)
        elif opc == "3":
            agregar_categoria(categoria)
        elif opc == "4":
            modificar_categoria(categoria)
        elif opc == "5":
            eliminar_categoria(categoria)
        elif opc == "0":
            activo = False

def menu_presupuestos(presupuestos, categoria, gastos, encabezadosP):
    activo = True
    opciones = [
        "Mostrar todos los presupuestos",
        "Consultar / Buscar presupuesto",
        "Agregar presupuesto",
        "Modificar presupuesto",
        "Baja / Reactivación lógica de presupuesto",
    ]
    while activo:
        mostrar_menu("GESTIÓN DE PRESUPUESTOS", opciones)
        opc = pedir_opcion_menu("Seleccione una opción:", ["0", "1", "2", "3", "4", "5"])

        if opc == "1":
            mostrar_presupuestos(presupuestos, categoria, encabezadosP)
        elif opc == "2":
            consultar_presupuesto(presupuestos, categoria, gastos, encabezadosP)
        elif opc == "3":
            agregar_presupuesto(presupuestos, categoria)
        elif opc == "4":
            modificar_presupuesto(presupuestos, categoria)
        elif opc == "5":
            eliminar_presupuesto(presupuestos, categoria)
        elif opc == "0":
            activo = False

def menu_gastos(gastos, categoria, presupuestos, encabezadosG):
    activo = True
    opciones = [
        "Mostrar todos los gastos",
        "Consultar / Buscar gasto específico",
        "Registrar nuevo gasto",
        "Modificar gasto",
        "Baja / Reactivación lógica de gasto",
        "Consultar gastos por rango de fechas",
    ]
    while activo:
        mostrar_menu("GESTIÓN DE GASTOS", opciones)
        opc = pedir_opcion_menu("Seleccione una opción:", ["0", "1", "2", "3", "4", "5", "6"])

        if opc == "1":
            mostrar_gastos(gastos, categoria, encabezadosG)
        elif opc == "2":
            consultar_gasto(gastos, categoria, presupuestos, encabezadosG)
        elif opc == "3":
            agregar_gasto(gastos, categoria, presupuestos)
        elif opc == "4":
            modificar_gasto(gastos, categoria)
        elif opc == "5":
            eliminar_gasto(gastos, categoria)
        elif opc == "6":
            consultar_gastos_por_rango_fechas(gastos, categoria, encabezadosG)
        elif opc == "0":
            activo = False

def menu_estadisticas(gastos, categoria, presupuestos, encabezadosG):
    activo = True
    opciones = [
        "Resumen Estadístico General Consolidado",
        "Reporte de Promedios (General y por Categoría)",
        "Conteo de Registros Totales y por Categoría",
        "Porcentajes Relativos de Gasto por Categoría",
        "Identificación de Valores Máximos y Mínimos",
        "Comparativa Gasto Real vs. Presupuesto Previsto",
        "Ordenamiento dinámico de gastos",
        "Estimación de variación e inflación",
    ]
    while activo:
        mostrar_menu("REPORTES Y ESTADÍSTICAS DEL SISTEMA", opciones)
        opc = pedir_opcion_menu("Seleccione una opción:", ["0", "1", "2", "3", "4", "5", "6", "7", "8"])

        if opc == "1":
            mostrar_resumen_estadistico_completo(gastos, categoria, presupuestos)
        elif opc == "2":
            mostrar_promedios(gastos, categoria)
        elif opc == "3":
            mostrar_conteos(gastos, categoria)
        elif opc == "4":
            mostrar_porcentajes_relativos(gastos, categoria)
        elif opc == "5":
            mostrar_maximos_y_minimos(gastos, categoria)
        elif opc == "6":
            comparativa_gastos_vs_presupuestos(gastos, categoria, presupuestos)
        elif opc == "7":
            ordenar_gastos_interactivo(gastos, categoria)
        elif opc == "8":
            simulacion_proyeccion_inflacion(gastos)
        elif opc == "0":
            activo = False

def menu_usuarios(usuario_actual=None):
    activo = True
    opciones = [
        "Listar usuarios registrados",
        "Registrar nuevo usuario",
        "Modificar permisos de usuario o rol",
        "Baja / Reactivación lógica de usuario",
    ]
    while activo:
        mostrar_menu("ADMINISTRACIÓN DE USUARIOS Y PERMISOS", opciones)
        opc = pedir_opcion_menu("Seleccione una opción:", ["0", "1", "2", "3", "4"])

        if opc == "1":
            listar_usuarios()
        elif opc == "2":
            registrar_usuario()
        elif opc == "3":
            modificar_permisos()
        elif opc == "4":
            eliminar_usuario(usuario_actual)
        elif opc == "0":
            activo = False

def menu_principal(usuario, categoria, presupuestos, gastos, encabezadosC, encabezadosP, encabezadosG):
    ejecutando = True

    modulos = [
        ("gastos", "Gestión de Gastos (CRUD)"),
        ("presupuestos", "Gestión de Presupuestos (CRUD)"),
        ("categorias", "Gestión de Categorías (CRUD)"),
        ("reportes", "Reportes y Estadísticas Financieras"),
        ("usuarios", "Administración de Usuarios y Permisos"),
    ]

    while ejecutando:
        disponibles = []
        for i in range(len(modulos)):
            permiso, texto = modulos[i]
            if verificar_permiso(usuario, permiso):
                disponibles.append((permiso, texto))

        opciones_texto = [d[1] for d in disponibles]
        mostrar_menu("SISTEMA DE CONTROL DE GASTOS PERSONALES Y FAMILIARES", opciones_texto)

        opciones_validas = ["0"]
        for i in range(len(disponibles)):
            opciones_validas.append(str(i + 1))

        opcion = pedir_opcion_menu("Seleccione una opción:", opciones_validas)

        if opcion == "0":
            mostrar_mensaje("¡Gracias por utilizar el sistema! Sesión finalizada.", "info")
            ejecutando = False
        else:
            indice = int(opcion) - 1
            permiso_elegido = disponibles[indice][0]

            if permiso_elegido == "gastos":
                menu_gastos(gastos, categoria, presupuestos, encabezadosG)
            elif permiso_elegido == "presupuestos":
                menu_presupuestos(presupuestos, categoria, gastos, encabezadosP)
            elif permiso_elegido == "categorias":
                menu_categorias(categoria, gastos, presupuestos, encabezadosC, encabezadosG)
            elif permiso_elegido == "reportes":
                menu_estadisticas(gastos, categoria, presupuestos, encabezadosG)
            elif permiso_elegido == "usuarios":
                menu_usuarios(usuario)

# =============================================================================
# 11. PUNTO DE ENTRADA
# =============================================================================

def main():
    usuario = login()
    if usuario:
        menu_principal(
            usuario,
            categoria,
            presupuestos,
            gastos,
            encabezadosC,
            encabezadosP,
            encabezadosG
        )
if __name__ == "__main__":
    main()