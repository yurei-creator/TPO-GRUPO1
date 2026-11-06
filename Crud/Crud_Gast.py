import json
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
    obtener_presupuesto_por_categoria
)
from Datos.Datos import categoria_ruta, presupuesto_ruta, ruta_gastos
from rich.table import Table
from rich.panel import Panel



def gastos_a_matriz(gastos):
    return [[g["id"], g["fecha"], g["monto"], g["categoria_id"], g["descripcion"], g["estado"]] for g in gastos]
# de JSON a python, lee los gastos del archivo.
def leer_gastos():
    try:
        with open(ruta_gastos, "r", encoding="UTF-8") as datos:
            return json.load(datos)
    except (FileNotFoundError, OSError, json.JSONDecodeError) as error:
        mostrar_mensaje(f"No se pudo leer el archivo {ruta_gastos}: {error}", "error")
        return None

# de python a JSON, sobrescribe el archivo con los gastos actualizados
def guardar_gastos(gastos):
    try:
        with open(ruta_gastos, "w", encoding="UTF-8") as datos:
            json.dump(gastos, datos, ensure_ascii=False, indent=4)
        return True
    except (FileNotFoundError, OSError) as error:
        mostrar_mensaje(f"No se pudo guardar el archivo {ruta_gastos}: {error}", "error")
        return False


def cargar_matriz(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return [linea.strip().split("|") for linea in archivo if linea.strip()]
    except OSError as error:
        mostrar_mensaje(f"No se pudo leer el archivo {ruta}: {error}", "alerta")
        return []

def mostrar_gastos():
    gastos = leer_gastos()
    if gastos is None:
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return
    categorias = cargar_matriz(categoria_ruta)

    filas = []
    for g in gastos:
        nom_cat = obtener_nombre_categoria(g["categoria_id"], categorias)
        monto_fmt = f"${float(g['monto']):,.2f}"
        filas.append([g["id"], g["fecha"], monto_fmt, nom_cat, g["descripcion"], g["estado"]])

    encs = ["ID", "Fecha", "Monto", "Categoría", "Descripción", "Estado"]
    renderizar_tabla(encs, filas, "Control General de Gastos")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def agregar_gasto():
    console.print("\n[bold green]--- [C] REGISTRAR NUEVO GASTO ---[/bold green]")
    gastos = leer_gastos()
    if gastos is None:
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return
    categorias = cargar_matriz(categoria_ruta)
    presupuestos = cargar_matriz(presupuesto_ruta)

    id_cat = seleccionar_categoria_id(categorias)
    if not id_cat:
        return

    descripcion = pedir_texto_no_vacio("Ingrese concepto / descripción del gasto:")
    monto = pedir_monto("Ingrese monto del gasto:")
    fecha = solicitar_y_verificar_fecha("Fecha del gasto (DD/MM/AAAA):")

    ids_existentes = [int(g["id"]) for g in gastos if g["id"].isdigit()]
    nuevo_id = str(max(ids_existentes) + 1) if ids_existentes else "1"

    nuevo_gasto = {
        "id": nuevo_id,
        "fecha": fecha,
        "monto": monto,
        "categoria_id": id_cat,
        "descripcion": descripcion,
        "estado": "Activo"
    }
    gastos.append(nuevo_gasto)

    # Sobrescribir el archivo con los datos actualizados
    if not guardar_gastos(gastos):
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    nom_cat = obtener_nombre_categoria(id_cat, categorias)
    mostrar_mensaje(f"Gasto registrado exitosamente con ID: {nuevo_id} por ${monto:,.2f} en '{nom_cat}'.", "exito")

    # Alerta de presupuesto si corresponde
    pres = obtener_presupuesto_por_categoria(id_cat, presupuestos)
    if pres:
        limite = float(pres[3])
        total_acumulado = sum([float(g["monto"]) for g in gastos if g["categoria_id"] == id_cat and g["estado"] == "Activo"])
        if total_acumulado > limite:
            exceso = total_acumulado - limite
            mostrar_mensaje(f"¡ATENCIÓN! Se ha superado el presupuesto para '{nom_cat}' por ${exceso:,.2f} (Límite: ${limite:,.2f} | Consumo actual: ${total_acumulado:,.2f}).", "alerta")
        else:
            disponible = limite - total_acumulado
            console.print(f"[dim]Presupuesto restante en {nom_cat}: ${disponible:,.2f} (Límite: ${limite:,.2f})[/dim]")

    console.input("[dim]Presione ENTER para continuar...[/dim]")

def consultar_gasto():
    console.print("\n[bold yellow]--- [R] CONSULTAR GASTO ESPECÍFICO ---[/bold yellow]")
    gastos = leer_gastos()
    if gastos is None:
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return
    categorias = cargar_matriz(categoria_ruta)
    presupuestos = cargar_matriz(presupuesto_ruta)

    if not gastos:
        mostrar_mensaje("No hay gastos registrados en el sistema.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    busqueda = pedir_texto_no_vacio("Ingrese término de búsqueda (ID, descripción o categoría):").lower()
    coincidencias = []

    for g in gastos:
        nom_c = obtener_nombre_categoria(g["categoria_id"], categorias).lower()
        if busqueda == g["id"].lower() or busqueda in g["descripcion"].lower() or busqueda in nom_c:
            coincidencias.append(g)

    if not coincidencias:
        mostrar_mensaje("No se encontraron gastos que coincidan con la búsqueda.", "alerta")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    for g in coincidencias:
        cat_info = obtener_categoria_por_id(g["categoria_id"], categorias)
        nom_cat = cat_info[1] if cat_info else "Sin Categoría"
        desc_cat = cat_info[2] if cat_info else "-"

        pres_info = obtener_presupuesto_por_categoria(g["categoria_id"], presupuestos)
        pres_str = f"${float(pres_info[3]):,.2f} ({pres_info[2]})" if pres_info else "Sin presupuesto asignado"

        panel_info = (
            f"[bold white]ID del Gasto:[/bold white] {g['id']}\n"
            f"[bold white]Fecha:[/bold white] {g['fecha']}\n"
            f"[bold white]Monto:[/bold white] [green]${float(g['monto']):,.2f}[/green]\n"
            f"[bold white]Descripción:[/bold white] {g['descripcion']}\n"
            f"[bold white]Estado:[/bold white] {g['estado']}\n"
            f"--------------------------------------------------\n"
            f"[bold cyan]Datos de la Categoría Asociada:[/bold cyan]\n"
            f"  • Nombre: {nom_cat} (ID {g['categoria_id']})\n"
            f"  • Detalle: {desc_cat}\n"
            f"[bold cyan]Presupuesto de la Categoría:[/bold cyan]\n"
            f"  • {pres_str}"
        )
        console.print(Panel(panel_info, title=f"[bold magenta]Gasto #{g['id']}[/bold magenta]", border_style="cyan"))

    console.input("[dim]Presione ENTER para continuar...[/dim]")

def consultar_gastos_por_rango_fechas():
    console.print("\n[bold cyan]--- CONSULTA DE GASTOS POR RANGO DE FECHAS ---[/bold cyan]")
    gastos = leer_gastos()
    if gastos is None:
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return
    categorias = cargar_matriz(categoria_ruta)

    f_inicio = solicitar_y_verificar_fecha("Ingrese fecha inicial (DD/MM/AAAA):")
    f_fin = solicitar_y_verificar_fecha("Ingrese fecha final (DD/MM/AAAA):")

    try:
        resultados = filtrar_por_fechas_recursivo(gastos, f_inicio, f_fin)
    except RecursionError:
        mostrar_mensaje("Hay demasiados registros para filtrar de forma recursiva (límite de recursión superado).", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return
    except (KeyError, ValueError, TypeError, IndexError):
        mostrar_mensaje("Se encontró un gasto con datos inválidos en gastos.json.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    if not resultados:
        mostrar_mensaje(f"No se registraron gastos activos entre el {f_inicio} y el {f_fin}.", "alerta")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    try:
        total_periodo = sumar_montos_recursivo(resultados)
    except RecursionError:
        mostrar_mensaje("Demasiados registros para sumar de forma recursiva; se calcula de forma iterativa.", "alerta")
        total_periodo = sum(float(g["monto"]) for g in resultados)
    except (KeyError, ValueError, TypeError):
        mostrar_mensaje("Algún gasto tiene un monto inválido; no se puede calcular el total.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    filas = []
    for g in resultados:
        nom_cat = obtener_nombre_categoria(g["categoria_id"], categorias)
        filas.append([g["id"], g["fecha"], f"${float(g['monto']):,.2f}", nom_cat, g["descripcion"]])

    encs = ["ID", "Fecha", "Monto", "Categoría", "Descripción"]
    renderizar_tabla(encs, filas, f"Gastos Registrados ({f_inicio} al {f_fin})")
    console.print(Panel(f"[bold white]Gasto Total en el Período Evaluado:[/bold white] [bold green]${total_periodo:,.2f}[/bold green]", border_style="green"))
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def modificar_gasto():
    console.print("\n[bold blue]--- [U] MODIFICAR GASTO ---[/bold blue]")
    gastos = leer_gastos()
    if gastos is None:
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return
    categorias = cargar_matriz(categoria_ruta)

    activos = [g for g in gastos if g["estado"] == "Activo"]
    if not activos:
        mostrar_mensaje("No hay gastos activos para modificar.", "alerta")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    for i in range(len(activos)):
        g = activos[i]
        nom_c = obtener_nombre_categoria(g["categoria_id"], categorias)
        console.print(f"  [yellow]{i + 1}[/yellow]. ID {g['id']} - {g['fecha']} | ${float(g['monto']):,.2f} | {nom_c} - {g['descripcion']}")

    opciones = [str(i + 1) for i in range(len(activos))]
    opciones.append("0")
    opc = pedir_opcion_menu("Seleccione el gasto a modificar (0 para cancelar):", opciones)
    if opc == "0":
        return

    idx = int(opc) - 1
    g_sel = activos[idx]

    console.print("\n[dim]Presione ENTER para conservar el dato actual:[/dim]")
    g_sel["descripcion"] = pedir_opcional("Nueva descripción", g_sel["descripcion"])
    g_sel["monto"] = pedir_monto_opcional("Nuevo monto", g_sel["monto"])
    g_sel["fecha"] = solicitar_fecha_opcional("Nueva fecha", g_sel["fecha"])

    cambiar_cat = pedir_texto_no_vacio("¿Desea reasignar la categoría? (s/n):").lower()
    if cambiar_cat == "s":
        nuevo_id_cat = seleccionar_categoria_id(categorias)
        if nuevo_id_cat:
            g_sel["categoria_id"] = nuevo_id_cat

    cambiar_est = pedir_texto_no_vacio(f"¿Cambiar estado actual ({g_sel['estado']})? (s/n):").lower()
    if cambiar_est == "s":
        g_sel["estado"] = "Inactivo" if g_sel["estado"] == "Activo" else "Activo"
        mostrar_mensaje(f"Estado modificado a: {g_sel['estado']}", "info")

    if guardar_gastos(gastos):
        mostrar_mensaje("Gasto modificado exitosamente.", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def eliminar_gasto():
    console.print("\n[bold red]--- [D] BAJA / REACTIVACIÓN LÓGICA DE GASTO ---[/bold red]")
    gastos = leer_gastos()
    if gastos is None:
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return
    categorias = cargar_matriz(categoria_ruta)

    if not gastos:
        mostrar_mensaje("No hay gastos registrados.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    for i in range(len(gastos)):
        g = gastos[i]
        nom_c = obtener_nombre_categoria(g["categoria_id"], categorias)
        col_est = "green" if g["estado"] == "Activo" else "red"
        console.print(f"  [yellow]{i + 1}[/yellow]. ID {g['id']} - {g['fecha']} | ${float(g['monto']):,.2f} | {nom_c} - {g['descripcion']} [{col_est}]({g['estado']})[/{col_est}]")

    opciones = [str(i + 1) for i in range(len(gastos))]
    opciones.append("0")
    opc = pedir_opcion_menu("Seleccione el gasto a cambiar estado (0 para cancelar):", opciones)
    if opc == "0":
        return

    idx = int(opc) - 1
    g = gastos[idx]

    if g["estado"] == "Inactivo":
        reactivar = pedir_texto_no_vacio(f"El gasto '{g['descripcion']}' (${float(g['monto']):,.2f}) está INACTIVO. ¿Desea reactivarlo? (s/n):").lower()
        if reactivar == "s":
            g["estado"] = "Activo"
            if guardar_gastos(gastos):
                mostrar_mensaje("Gasto reactivado correctamente.", "exito")
        else:
            mostrar_mensaje("Operación cancelada.", "info")
    else:
        confirmar = pedir_texto_no_vacio(f"¿Confirmar baja lógica del gasto '{g['descripcion']}' (${float(g['monto']):,.2f})? (s/n):").lower()
        if confirmar == "s":
            g["estado"] = "Inactivo"
            if guardar_gastos(gastos):
                mostrar_mensaje("Gasto dado de baja correctamente (Inactivo).", "exito")
        else:
            mostrar_mensaje("Operación cancelada.", "info")

    console.input("[dim]Presione ENTER para continuar...[/dim]")
