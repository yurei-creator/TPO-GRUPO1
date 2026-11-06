import re
from .Func_Rich import console, mostrar_mensaje

def pedir_monto(mensaje):
    while True:
        entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] ").strip()
        if not entrada:
            mostrar_mensaje("El campo no puede estar vacío.", "error")
            continue
            
        try:
            valor = float(entrada.replace(",", "."))
            if valor <= 0:
                mostrar_mensaje("El monto debe ser un número mayor a cero.", "alerta")
                continue
            return valor
        except ValueError:
            mostrar_mensaje("El formato ingresado no es un número válido.", "error")

def pedir_monto_opcional(mensaje, valor_actual):
    while True:
        entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] [yellow][${valor_actual}][/yellow]: ").strip()
        if not entrada:
            return float(valor_actual)
            
        try:
            valor = float(entrada.replace(",", "."))
            if valor <= 0:
                mostrar_mensaje("El monto debe ser mayor a cero.", "alerta")
                continue
            return valor
        except ValueError:
            mostrar_mensaje("El formato ingresado no es un número válido.", "error")

def es_fecha_valida(fecha_str):
    try:
        patron = r"^\d{2}/\d{2}/\d{4}$"
        if not re.match(patron, fecha_str):
            raise ValueError("Formato inválido")
        
        dia = int(fecha_str[0:2])
        mes = int(fecha_str[3:5])
        anio = int(fecha_str[6:10])
        
        rango_anios = (1900, 2100)
        if anio < rango_anios[0] or anio > rango_anios[1] or mes < 1 or mes > 12:
            raise ValueError("Año o mes fuera de rango")
            
        es_bisiesto = (anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0))
        
        dias_por_mes = (31, 29 if es_bisiesto else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        
        if dia < 1 or dia > dias_por_mes[mes - 1]:
            raise ValueError("Día fuera de rango para el mes")
            
        return True
    except (ValueError, IndexError):
        return False

def solicitar_y_verificar_fecha(mensaje="Ingrese fecha (DD/MM/AAAA):"):
    while True:
        entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] ").strip()
        if not es_fecha_valida(entrada):
            mostrar_mensaje("Fecha inválida en el calendario. Use el formato DD/MM/AAAA.", "error")
            continue
        return entrada

def solicitar_fecha_opcional(mensaje, fecha_actual):
    while True:
        entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] [yellow][{fecha_actual}][/yellow]: ").strip()
        if not entrada:
            return fecha_actual
            
        if not es_fecha_valida(entrada):
            mostrar_mensaje("Fecha inválida en el calendario. Use el formato DD/MM/AAAA.", "error")
            continue
        return entrada

def pedir_texto_no_vacio(mensaje):
    while True:
        entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] ").strip()
        if not entrada:
            mostrar_mensaje("Este campo no puede estar vacío.", "error")
            continue
        return entrada

def pedir_opcional(mensaje, valor_actual):
    try:
        entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] [yellow][{valor_actual}][/yellow]: ").strip()
        if len(entrada) > 0:
            return entrada
        return valor_actual
    except (EOFError, KeyboardInterrupt):
        return valor_actual

def pedir_opcion_menu(mensaje, opciones_validas):
    while True:
        entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] ").strip()
        if not entrada:
            mostrar_mensaje("Debe ingresar una opción.", "error")
            continue
            
        try:
            int(entrada)
            if entrada not in opciones_validas:
                mostrar_mensaje("Opción fuera de rango.", "error")
                continue
            return entrada
        except ValueError:
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
    try:
        idx_seleccionada = int(opc) - 1
        return activas[idx_seleccionada][0]
    except (ValueError, IndexError):
        mostrar_mensaje("Error al seleccionar la categoría.", "error")
        return None

def fecha_a_numero(fecha_str):
    try:
        anio = fecha_str[6:10]
        mes = fecha_str[3:5]
        dia = fecha_str[0:2]
        return int(f"{anio}{mes}{dia}")
    except (ValueError, IndexError):
        return 0

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