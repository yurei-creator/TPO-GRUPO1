from Func_Rich import console, mostrar_mensaje

from datosprincipales import (
    Id_Categoria, NombreC, DescripcionC, EstadoC, 
    Id_Gasto, NombreG, DescripcionG, EstadoG, 
    Id_Presupuesto, Periodo_Presupuesto, Monto_limite, Id_CategoriaP, EstadoP
)

def pedir_monto(mensaje):
    monto_valido = False
    resultado = 0.0
    while not monto_valido:
        entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] ").strip()
        if len(entrada) == 0:
            mostrar_mensaje("El campo no puede estar vacío.", "error")
        else:
            entrada_normalizada = entrada.replace(",", ".")
            partes = entrada_normalizada.split(".")
            es_num = False
            if len(partes) == 1 and partes[0].isdigit():
                es_num = True
            elif len(partes) == 2 and (partes[0].isdigit() or partes[0] == "") and partes[1].isdigit():
                if not (partes[0] == "" and len(partes[1]) == 0):
                    es_num = True
            if es_num:
                valor = float(entrada_normalizada)
                if valor > 0:
                    resultado = valor
                    monto_valido = True
                else:
                    mostrar_mensaje("El monto debe ser un número mayor a cero.", "alerta")
            else:
                mostrar_mensaje("Error: el formato introducido no es un número válido.", "error")
    return resultado

def pedir_monto_opcional(mensaje, valor_actual):
    monto_valido = False
    resultado = float(valor_actual)
    while not monto_valido:
        entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] [yellow][${valor_actual}][/yellow]: ").strip()
        if len(entrada) == 0:
            monto_valido = True
        else:
            entrada_normalizada = entrada.replace(",", ".")
            partes = entrada_normalizada.split(".")
            es_num = False
            if len(partes) == 1 and partes[0].isdigit():
                es_num = True
            elif len(partes) == 2 and (partes[0].isdigit() or partes[0] == "") and partes[1].isdigit():
                if not (partes[0] == "" and len(partes[1]) == 0):
                    es_num = True
            if es_num:
                valor = float(entrada_normalizada)
                if valor > 0:
                    resultado = valor
                    monto_valido = True
                else:
                    mostrar_mensaje("El monto debe ser un número mayor a cero.", "alerta")
            else:
                mostrar_mensaje("Error: el formato introducido no es un número válido.", "error")
    return resultado

def solicitar_y_verificar_fecha():
    fecha_valida = False
    resultado_fecha = ""
    while not fecha_valida:
        entrada = console.input("[bold cyan]Ingresa la fecha (DD/MM/AAAA):[/bold cyan] ").strip()
        partes = entrada.split("/")
        if len(partes) == 3 and partes[0].isdigit() and partes[1].isdigit() and partes[2].isdigit():
            dia = int(partes[0])
            mes = int(partes[1])
            anio = int(partes[2])
            es_bisiesto = anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)
            dias_por_mes = [31, 29 if es_bisiesto else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if 1 <= mes <= 12 and 1 <= dia <= dias_por_mes[mes - 1] and anio > 0:
                resultado_fecha = f"{dia:02d}/{mes:02d}/{anio:04d}"
                fecha_valida = True
            else:
                mostrar_mensaje("Fecha inválida en el calendario.", "error")
        else:
            mostrar_mensaje("Formato incorrecto. Use DD/MM/AAAA.", "error")
    return resultado_fecha

def pedir_texto_no_vacio(mensaje):
    texto_valido = False
    resultado = ""
    while not texto_valido:
        entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] ").strip()
        if len(entrada) > 0:
            resultado = entrada
            texto_valido = True
        else:
            mostrar_mensaje("Este campo no puede estar vacío.", "error")
    return resultado

def pedir_opcional(mensaje, valor_actual):
    entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] [yellow][{valor_actual}][/yellow]: ").strip()
    resultado = valor_actual
    if len(entrada) > 0:
        resultado = entrada
    return resultado

def pedir_id_existente(mensaje, lista_ids, lista_estados):
    id_valido = False
    resultado_id = ""
    while not id_valido:
        entrada = pedir_texto_no_vacio(mensaje)
        encontrado = False
        for i in range(len(lista_ids)):
            if lista_ids[i] == entrada and str(lista_estados[i]).upper() == "ACTIVO":
                encontrado = True
        if encontrado:
            resultado_id = entrada
            id_valido = True
        else:
            mostrar_mensaje("El ID ingresado no existe o no está activo.", "error")
    return resultado_id

def obtener_nombre_categoria(id_cat):
    for i in range(len(Id_Categoria)):
        if Id_Categoria[i] == str(id_cat):
            return NombreC[i]
    return "Sin Categoría"

def obtener_periodo_presupuesto(id_pres):
    for i in range(len(Id_Presupuesto)):
        if Id_Presupuesto[i] == str(id_pres):
            return Periodo_Presupuesto[i]
    return "Sin Presupuesto"

def seleccionar_categoria():
    console.print("\n[bold cyan]Seleccione una Categoría:[/bold cyan]")
    activas_idx = []
    for i in range(len(NombreC)):
        if str(EstadoC[i]).upper() == "ACTIVO":
            activas_idx.append(i)
            console.print(f"  [yellow]{len(activas_idx)}[/yellow]. {NombreC[i]} ({DescripcionC[i]})")
    
    valido = False
    id_seleccionado = ""
    while not valido:
        opc = pedir_texto_no_vacio("Ingrese el número de la categoría: ")
        if opc.isdigit():
            num = int(opc)
            if 1 <= num <= len(activas_idx):
                idx_real = activas_idx[num - 1]
                id_seleccionado = Id_Categoria[idx_real]
                valido = True
            else:
                mostrar_mensaje("Número fuera de rango.", "error")
        else:
            mostrar_mensaje("Debe ingresar un número.", "error")
    return id_seleccionado

def seleccionar_gasto():
    console.print("\n[bold cyan]Seleccione un Gasto:[/bold cyan]")
    activas_idx = []
    for i in range(len(NombreG)):
        if str(EstadoC[i]).upper() == "ACTIVO":
            activas_idx.append(i)
            console.print(f"  [yellow]{len(activas_idx)}[/yellow]. {NombreG[i]} ({DescripcionG[i]})")
    
    valido = False
    id_seleccionado = ""
    while not valido:
        opc = pedir_texto_no_vacio("Ingrese el número de la categoría: ")
        if opc.isdigit():
            num = int(opc)
            if 1 <= num <= len(activas_idx):
                idx_real = activas_idx[num - 1]
                id_seleccionado = Id_Gasto[idx_real]
                valido = True
            else:
                mostrar_mensaje("Número fuera de rango.", "error")
        else:
            mostrar_mensaje("Debe ingresar un número.", "error")
    return id_seleccionado

def seleccionar_presupuesto():
    console.print("\n[bold cyan]Seleccione un Presupuesto:[/bold cyan]")
    activas_idx = []
    for i in range(len(Periodo_Presupuesto)):
        if str(EstadoP[i]).upper() == "ACTIVO":
            activas_idx.append(i)
            cat_nom = obtener_nombre_categoria(Id_CategoriaP[i])
            console.print(f"  [yellow]{len(activas_idx)}[/yellow]. {cat_nom} | Período: {Periodo_Presupuesto[i]} (Límite: ${Monto_limite[i]})")
    
    valido = False
    id_seleccionado = ""
    while not valido:
        opc = pedir_texto_no_vacio("Ingrese el número del presupuesto: ")
        if opc.isdigit():
            num = int(opc)
            if 1 <= num <= len(activas_idx):
                idx_real = activas_idx[num - 1]
                id_seleccionado = Id_Presupuesto[idx_real]
                valido = True
            else:
                mostrar_mensaje("Número fuera de rango.", "error")
        else:
            mostrar_mensaje("Debe ingresar un número.", "error")
    return id_seleccionado