#--------------------------LISTAS GASTOS--------------------------------------------#

NombreG = ["Supermercado", "Gasolina", "Cine", "Farmacia", "Curso online"]

MontoG = [120, 45, 25, 15.50, 80]

FechaG = ["01/08/2026", "02/08/2026", "03/08/2026", "04/08/2026", "05/08/2026"]

CategoriaG = ["Alimentos", "Transporte", "Ocio", "Salud", "Educación"]

DescripcionG = [
    "Compra mensual de viveres", 
    "Tanque lleno del auto", 
    "Entradas y palomitas", 
    "Medicamentos para la gripe", 
    "Inscripción a taller de Excel"
]

EstadoG = [True, True, True, True, True]

gastos = [NombreG,MontoG,FechaG, CategoriaG, DescripcionG, EstadoG]

#--------------------------LISTAS PRESUPUESTOS--------------------------------------------#
NombreP = ["Limite Alimentos", "Limite Transporte", "Limite Ocio", "Limite Salud", "Limite Educación"]

MontoP = [400, 150, 100, 80, 120]

FechaP = ["01/08/2026", "01/08/2026", "01/08/2026", "01/08/2026", "01/08/2026"]

CategoriaP = ["Alimentos", "Transporte", "Ocio", "Salud", "Educación"]

DescripcionP = [
    "Presupuesto maximo del mes", 
    "Estimado para pasajes y gasolina", 
    "Dinero para salidas y diversion", 
    "Reservas para emergencias medicas", 
    "Libros y materiales de estudio"
]

EstadoP = [True, True, True, True, True]

presupuestos = [NombreP, MontoP, FechaP, CategoriaP, DescripcionP, EstadoP]

# Encabezados
encabezadosG = ["Gastos", "Monto", "Fecha", "Categoria", "Descripcion"]
encabezadosP = ["Presupuestos", "Monto", "Fecha", "Categoria", "Descripcion"]

# CREACION Y LLENADO DINÁMICO DE MATRICES

def obtener_matriz(lista):
    matriz = []

    for col in range(len(lista[0])):
        fila = [
            lista[0][col],
            lista[1][col],
            lista[2][col],
            lista[3][col],
            lista[4][col],
            "Activo" if lista[5][col] else "Inactivo"
        ]

        matriz.append(fila)
    return matriz

# MOSTRAR MATRICES
def mostrar_matriz(matriz, encabezados):
    if not matriz:
        print("No hay datos cargados.")
        return

    filas = len(matriz)
    columnas = len(encabezados)
    anchos = []

    for col in range(columnas):
        ancho = len(encabezados[col])
        for fila in range(filas):
            estado = matriz[fila][-1]
            if estado == "ACTIVO" or estado == "Activo":
                valor = str(matriz[fila][col])
                if len(valor) > ancho:
                    ancho = len(valor)
            anchos.append(ancho)

    for col in range(columnas):
        titulo = encabezados[col]
        espacios = " " * (anchos[col] - len(titulo))
        print(titulo + espacios + "  ", end="")
    print()

    for fila in range(filas):
        estado = matriz[fila][-1]
        if estado == "ACTIVO" or estado == "Activo":
            for col in range(columnas):
                valor = str(matriz[fila][col])
                espacios = " " * (anchos[col] - len(valor))
                print(valor + espacios + "  ", end="")  
            print()
    print()  # Línea en blanco después de la matriz
    input("Presione ENTER para continuar...")
# INGRESO Y VALIDACIÓN DE DATOS
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
def pedir_monto_int(mensaje):
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
                if monto_final > 0 and monto_final.is_integer():
                    dato_invalido = False
                    return int(monto_final)
                else: 
                    print("El monto debe ser un número entero mayor a cero.")
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

def consultar_gasto():
    print("\n--- [R] CONSULTAR / BUSCAR GASTOS ---")
    if not NombreG:
        print("No hay gastos para consultar.")
        return

    busqueda_str = pedir_texto_no_vacio("Ingrese término de búsqueda (nombre, categoría o N° de fila): ")
    busqueda_lower = busqueda_str.lower()
    coincidencias = []
    print(f"DEBUG [INFO]: Se ingresó el término de búsqueda: {busqueda_str}")
    # Búsqueda por número de fila (1..N)
    numero = False
    if busqueda_str != "":
        for caracter in busqueda_str:
            if caracter >= "0" and caracter <= "9":
                numero = True
            elif caracter in ["abcdefghijklmnopqrstuvwxyz", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", " ", ".", ","]:
                numero = False
                
    if numero:
        num = int(busqueda_str)
        if 1 <= num <= len(NombreG):
            coincidencias.append(num - 1)
    
    # Búsqueda por texto (nombre o categoría)
    for i in range(len(NombreG)):
        if busqueda_lower in NombreG[i].lower() or busqueda_lower in CategoriaG[i].lower():
            if i not in coincidencias:
                coincidencias.append(i)
    print(f"DEBUG [INFO]: Se encontraron {len(coincidencias)} coincidencia(s) para el término '{busqueda_str}'.")
    if not coincidencias:
        print("No se encontraron gastos que coincidan con la búsqueda.")
    else:
        print(f"\nSe encontraron {len(coincidencias)} resultado(s):")
        encabezados = ["#", "Gasto", "Monto", "Fecha", "Categoría", "Descripción", "Estado"]
        matriz_res = []
        for idx in coincidencias:
            est = "Activo" if EstadoG[idx] else "Inactivo"
            matriz_res.append([idx + 1, NombreG[idx], MontoG[idx], FechaG[idx], CategoriaG[idx], DescripcionG[idx], est])
        mostrar_matriz(matriz_res,encabezados)
        input("Presione ENTER para continuar...")

def agregar_gasto():
    print("\n--- [C] AGREGAR NUEVO GASTO ---")
    nombre = pedir_texto_no_vacio_con_espacios("Ingrese nombre del gasto: ")
    monto = pedir_monto("Ingrese monto: ")
    fecha = solicitar_y_verificar_fecha()
    categoria = pedir_texto_no_vacio_con_espacios("Ingrese categoría: ")
    descripcion = pedir_texto_no_vacio_con_espacios("Ingrese descripción: ")

    NombreG.append(nombre)
    MontoG.append(monto)
    FechaG.append(fecha)
    CategoriaG.append(categoria)
    DescripcionG.append(descripcion)
    EstadoG.append(True)
    print("¡Gasto agregado exitosamente (Estado: Activo)!\n")
    input("Presione ENTER para continuar...")

def modificar_gasto():
    print("\n--- [U] MODIFICAR GASTO ---")


    opc = pedir_texto_no_vacio("Ingrese el número del gasto a modificar: ")
    while opc != "0" and (not opc.isdigit() or int(opc) < 1 or int(opc) > len(NombreG)):
        print("Número de gasto inválido. Intente nuevamente.")
        opc = pedir_texto_no_vacio("Ingrese el número del gasto a modificar: ")
    if opc == "0":
        print("Operación cancelada. No se realizaron cambios.")
        return
    idx = int(opc) - 1
    print(f"\nModificando gasto #{opc} (Presione ENTER para conservar el valor actual):")
    NombreG[idx] = pedir_opcional("Nuevo nombre", NombreG[idx])
    
    nuevo_monto = pedir_monto_opcional("Nuevo monto (actual: ${}): ".format(MontoG[idx]), MontoG[idx])
    if nuevo_monto != "":
        MontoG[idx] = nuevo_monto
    FechaG[idx] = pedir_opcional("Nueva fecha (DD/MM/AAAA)", FechaG[idx])
    CategoriaG[idx] = pedir_opcional("Nueva categoría", CategoriaG[idx])
    DescripcionG[idx] = pedir_opcional("Nueva descripción", DescripcionG[idx])

    estado_actual = "Activo" if EstadoG[idx] else "Inactivo"
    cambiar_est = input(f"¿Desea cambiar el estado actual ({estado_actual})? (s/n): ").strip().lower()
    if cambiar_est == 's':
        EstadoG[idx] = not EstadoG[idx]
        nuevo_est = "Activo" if EstadoG[idx] else "Inactivo"
        print(f"Estado cambiado a: {nuevo_est}")
    elif cambiar_est == 'n':
        print("Estado no modificado.")

    print("¡Gasto actualizado exitosamente!\n")
    print()
    input("Presione ENTER para continuar...")


def menu_gastos(matrizG, encabezadoG):
    menu = 1
    while menu == 1:
        print("\n========================================")
        print("         GESTIÓN DE GASTOS              ")
        print("========================================")
        print("1. Mostrar gastos")
        print("2. Consultar / Buscar gasto")
        print("3. Agregar nuevo gasto (Crear)")
        print("4. Modificar un gasto (Actualizar)")
        print("5. Dar de baja lógica un gasto")
        print("0. Volver al menú principal")
        print("========================================")
        opc = pedir_texto_no_vacio("Seleccione una opción: ")

        if opc == "1":
            matrizG = obtener_matriz(gastos)
            mostrar_matriz(matrizG, encabezadoG)
        elif opc == "2":
            consultar_gasto()
        elif opc == "3":
            agregar_gasto()
        elif opc == "4":
            modificar_gasto()
        elif opc == "5":
            eliminar_gasto()
        elif opc == "0":
            menu = 0
        else:
            print("Opción no válida. Intente nuevamente.")


def menu_principal(matrizG, encabezadoG, matrizP, encabezadoP):
    menu = 1
    while menu == 1:
        print("\n========================================")
        print("    SISTEMA DE GESTIÓN FINANCIERA       ")
        print("========================================")
        print("1. Gestión de Gastos (CRUD)")
        print("2. Gestión de Presupuestos (CRUD)")
        print("3. Ver Tablas Completas (Matrices)")
        print("0. Salir")
        print("========================================")
        opcion = pedir_texto_no_vacio("Seleccione una opción: ")

        if opcion == "1":
            menu_gastos(matrizG, encabezadoG)
        elif opcion == "2":
            menu_presupuestos(matrizP, encabezadoP)
        elif opcion == "3":
            mostrar_matriz(matrizG, encabezadoG)
            mostrar_matriz(matrizP, encabezadoP)
        elif opcion == "0":
            print("¡Gracias por utilizar el sistema! Hasta luego.")
            menu = 0
        else:
            print("Opción no válida. Por favor, intente nuevamente.\n")

if __name__ == "__main__":

    matrizG = obtener_matriz(gastos)
    matrizP = obtener_matriz(presupuestos)

    menu_principal(matrizG, encabezadosG, matrizP, encabezadosP)