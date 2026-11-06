import re
from .Func_Rich import console, mostrar_mensaje

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