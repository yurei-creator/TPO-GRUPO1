from .Func_Rich import mostrar_mensaje, console

def pedir_monto(mensaje):

    dato_invalido = True
    while dato_invalido:
        numero_valido = True
        monto = input(mensaje)
        puntos_encontrados = 0
        monto_limpio = ""
        
        if monto != "":
            for caracter in monto:
                if caracter == "." or caracter == ",":
                    puntos_encontrados += 1
                    monto_limpio += "."
                elif caracter >= "0" and caracter <= "9":
                    monto_limpio += caracter
                else:
                    numero_valido = False
            
            if puntos_encontrados > 1:
                numero_valido = False
                
            if monto_limpio == ".":
                numero_valido = False

            if numero_valido:
                monto_final = float(monto_limpio)
                if monto_final > 0:
                    dato_invalido = False
                    return monto_final
                else: 
                    print("El monto debe ser un número mayor a cero.")
            else:
                print("Error: el formato introducido no es un número válido.")
        else:
            print("El campo no puede estar vacío.")

def pedir_monto_opcional(mensaje, valor_actual):
    while True:
        monto = input(mensaje + f" [${valor_actual}]: ")
        if monto == "":
            return valor_actual
        puntos_encontrados = 0
        monto_limpio = ""
        numero_valido = True
        
        for caracter in monto:
            if caracter == "." or caracter == ",":
                puntos_encontrados += 1
                monto_limpio += "."
            elif caracter >= "0" and caracter <= "9":
                monto_limpio += caracter
            else:
                numero_valido = False
        
        if puntos_encontrados > 1:
            numero_valido = False
            
        if monto_limpio == ".":
            numero_valido = False

        if numero_valido:
            monto_final = float(monto_limpio)
            if monto_final > 0:
                return monto_final
            else: 
                print("El monto debe ser un número mayor a cero.")
        else:
            print("Error: el formato introducido no es un número válido.")

def solicitar_y_verificar_fecha():
    #pedir y verificar el dia
    dia = 0
    while dia < 1 or dia > 31:
        dia = int(input("Ingresa el día: "))
        if dia < 1 or dia > 31:
            print("Error: El día debe estar entre 1 y 31. Por favor, ingrese un valor válido.")

    #pedir y verificar el mes
    mes_valido = False
    while not mes_valido:
        mes = int(input("Ingresa el mes: "))
        
        if mes < 1 or mes > 12:
            print("Error: El mes debe estar entre 1 y 12. Por favor, ingrese un valor válido.")
        elif dia == 31 and mes in [4, 6, 9, 11]:
            print("Error: El mes ingresado solo tiene 30 días. Por favor, ingrese un valor válido.")
        elif dia >= 30 and mes == 2:
            print("Error: Febrero nunca puede tener 30 o 31 días. Por favor, ingrese un valor válido.")
        else:
            mes_valido = True

    #pedir y verificar el año
    anio_valido = False
    while not anio_valido:
        anio = int(input("Ingresa el año: "))
        
        # verificar si el año es bisiesto
        es_bisiesto = (anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0))

        if dia == 29 and mes == 2 and not es_bisiesto:
            print("Error: El año no es bisiesto, por lo que febrero no tiene 29 días.")
            print("Por favor, ingresá otro año válido:")
        else:
            anio_valido = True

    return f"{dia}/{mes}/{anio}"

def pedir_texto_no_vacio(mensaje):

    texto_sin_espacios = ""
    text = False
    while not text:
        texto = input(mensaje)
        if texto != "":
            for caracter in range(len(texto)):
                if texto[caracter] != " ":
                    texto_sin_espacios += texto[caracter]
            print("DEBUG [INFO]: Se ingresó el texto: " + texto_sin_espacios)
            return texto_sin_espacios
        else:
            print("[AVISO]: Este campo no puede estar vacío.")

def pedir_texto_no_vacio_con_espacios(mensaje):
    text = False
    while not text:
        texto = input(mensaje)
        if texto != "":
            print("DEBUG [INFO]: Se ingresó el texto: " + texto)
            return texto
        else:
            print("[AVISO]: Este campo no puede estar vacío.")            

def pedir_monto_opcional(mensaje, valor_actual):
    while True:
        monto = input(mensaje)
        if monto == "":
            return valor_actual
        puntos_encontrados = 0
        monto_limpio = ""
        numero_valido = True
        
        for caracter in monto:
            if caracter == "." or caracter == ",":
                puntos_encontrados += 1
                monto_limpio += "."
            elif caracter >= "0" and caracter <= "9":
                monto_limpio += caracter
            else:
                numero_valido = False
        
        if puntos_encontrados > 1:
            numero_valido = False
            
        if monto_limpio == ".":
            numero_valido = False

        if numero_valido:
            monto_final = float(monto_limpio)
            if monto_final > 0:
                return monto_final
            else: 
                print("El monto debe ser un número mayor a cero.")
        else:
            print("Error: el formato introducido no es un número válido.")

def pedir_opcional(mensaje, valor_actual):
    nuevo_valor = input(mensaje + f" [{valor_actual}]: ")
    if nuevo_valor == "":
        return valor_actual
    return nuevo_valor


# Selecciones

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

# Busquedas ?

def obtener_periodo_presupuesto(id_pres):
    for i in range(len(Id_Presupuesto)):
        if Id_Presupuesto[i] == str(id_pres):
            return Periodo_Presupuesto[i]
    return "Sin Presupuesto"

def obtener_nombre_categoria(lista_id,id_buscado,lista_nombres):
    for i in range(len(lista_id)):
        if lista_id[i] == str(id_buscado):
            return lista_nombres[i]
    return "Sin Categoría"

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
