#IGNOREN ESTE ARCHIVO
#IGNOREN ESTE ARCHIVO
#IGNOREN ESTE ARCHIVO



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






def mostrar_presupuestos():
    print("\n=================== MATRIZ DE PRESUPUESTOS ===================")
    matriz_p = obtener_matriz(presupuestos)
    mostrar_matriz(matriz_p, encabezadosP)
    print()

def mostrar_gastos():
    print("\n=================== MATRIZ DE GASTOS ===================")
    matriz_g = obtener_matriz(gastos)
    mostrar_matriz(matriz_g, encabezadosG)
    print()

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
    cambiar_est = pedir_texto_no_vacio(f"¿Desea cambiar el estado actual ({estado_actual})? (s/n): ").lower()
    if cambiar_est == 's':
        EstadoG[idx] = not EstadoG[idx]
        nuevo_est = "Activo" if EstadoG[idx] else "Inactivo"
        print(f"Estado cambiado a: {nuevo_est}")
    elif cambiar_est == 'n':
        print("Estado no modificado.")

    print("¡Gasto actualizado exitosamente!\n")
    print()
    input("Presione ENTER para continuar...")

def eliminar_gasto():
    print("\n--- [D] DAR DE BAJA LÓGICA GASTO ---")

    opc = pedir_texto_no_vacio("Ingrese el número del gasto a modificar: ")
    while opc != "0" and (not opc.isdigit() or int(opc) < 1 or int(opc) > len(NombreG)):
        print("Número de gasto inválido. Intente nuevamente.")
        opc = pedir_texto_no_vacio("Ingrese el número del gasto a modificar: ")
    if opc == "0":
        print("Operación cancelada. No se realizaron cambios.")
        return
    idx = int(opc) - 1

    if not EstadoG[idx]:
        print(f"El gasto '{NombreG[idx]}' ya se encuentra en estado INACTIVO.")
        reactivar = pedir_texto_no_vacio("¿Desea reactivarlo? (s/n): ").lower()
        if reactivar == 's':
            EstadoG[idx] = True
            print(f"¡Gasto '{NombreG[idx]}' reactivado (Activo) correctamente!\n")
        else:
            print("Operación cancelada.\n")
        return

    confirmacion = pedir_texto_no_vacio(f"¿Está seguro de dar de baja el gasto '{NombreG[idx]}' de ${MontoG[idx]}? (s/n): ").lower()
    if confirmacion == 's':
        EstadoG[idx] = False
        print(f"¡Gasto '{NombreG[idx]}' dado de baja correctamente (Estado: Inactivo)!\n")
    else:
        print("Operación cancelada.\n")
    input("Presione ENTER para continuar...")

def agregar_presupuesto():
    print("\n--- [C] AGREGAR NUEVO PRESUPUESTO ---")
    nombre = pedir_texto_no_vacio_con_espacios("Ingrese nombre del presupuesto: ")
    monto = pedir_monto("Ingrese monto límite: ")
    fecha = solicitar_y_verificar_fecha()
    categoria = pedir_texto_no_vacio_con_espacios("Ingrese categoría: ")
    descripcion = pedir_texto_no_vacio_con_espacios("Ingrese descripción: ")

    NombreP.append(nombre)
    MontoP.append(monto)
    FechaP.append(fecha)
    CategoriaP.append(categoria)
    DescripcionP.append(descripcion)
    EstadoP.append(True)
    print("¡Presupuesto agregado exitosamente (Estado: Activo)!\n")
    input("Presione ENTER para continuar...")

def consultar_presupuesto():
    print("\n--- [R] CONSULTAR / BUSCAR PRESUPUESTOS ---")
    if not NombreP:
        print("No hay presupuestos para consultar.")
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
        if 1 <= num <= len(NombreP):
            coincidencias.append(num - 1)
    
    # Búsqueda por texto (nombre o categoría)
    for i in range(len(NombreP)):
        if busqueda_lower in NombreP[i].lower() or busqueda_lower in CategoriaP[i].lower():
            if i not in coincidencias:
                coincidencias.append(i)
    print(f"DEBUG [INFO]: Se encontraron {len(coincidencias)} coincidencia(s) para el término '{busqueda_str}'.")
    if not coincidencias:
        print("No se encontraron presupuestos que coincidan con la búsqueda.")
    else:
        print(f"\nSe encontraron {len(coincidencias)} resultado(s):")
        encabezados = ["#", "Presupuesto", "Monto", "Fecha", "Categoría", "Descripción", "Estado"]
        matriz_res = []
        for idx in coincidencias:
            est = "Activo" if EstadoP[idx] else "Inactivo"
            matriz_res.append([idx + 1, NombreP[idx], MontoP[idx], FechaP[idx], CategoriaP[idx], DescripcionP[idx], est])
        mostrar_matriz(matriz_res,encabezados)


def modificar_presupuesto():
    print("\n--- [U] MODIFICAR PRESUPUESTO ---")


    opc = pedir_texto_no_vacio("Ingrese el número del presupuesto a modificar: ")
    while opc != "0" and (not opc.isdigit() or int(opc) < 1 or int(opc) > len(NombreP)):
        print("Número de presupuesto inválido. Intente nuevamente.")
        opc = pedir_texto_no_vacio("Ingrese el número del presupuesto a modificar: ")
    if opc == "0":
        print("Operación cancelada. No se realizaron cambios.")
        return
    idx = int(opc) - 1
    print(f"\nModificando presupuesto #{opc} (Presione ENTER para conservar el valor actual):")
    NombreP[idx] = pedir_opcional("Nuevo nombre", NombreP[idx])

    nuevo_monto = pedir_monto_opcional("Nuevo monto (actual: ${}): ".format(MontoP[idx]), MontoP[idx])
    if nuevo_monto != "":
        MontoP[idx] = nuevo_monto
    FechaP[idx] = pedir_opcional("Nueva fecha (DD/MM/AAAA)", FechaP[idx])
    CategoriaP[idx] = pedir_opcional("Nueva categoría", CategoriaP[idx])
    DescripcionP[idx] = pedir_opcional("Nueva descripción", DescripcionP[idx])

    estado_actual = "Activo" if EstadoP[idx] else "Inactivo"
    cambiar_est = pedir_texto_no_vacio(f"¿Desea cambiar el estado actual ({estado_actual})? (s/n): ").lower()
    if cambiar_est == 's':
        EstadoP[idx] = not EstadoP[idx]
        nuevo_est = "Activo" if EstadoP[idx] else "Inactivo"
        print(f"Estado cambiado a: {nuevo_est}")
    elif cambiar_est == 'n':
        print("Estado no modificado.")

    print("¡Presupuesto actualizado exitosamente!\n")
    print()
    input("Presione ENTER para continuar...")

def eliminar_presupuesto():
    print("\n--- [D] DAR DE BAJA LÓGICA PRESUPUESTO ---")

    opc = pedir_texto_no_vacio("Ingrese el número del presupuesto a dar de baja: ")
    while opc != "0" and (not opc.isdigit() or int(opc) < 1 or int(opc) > len(NombreP)):
        print("Número de presupuesto inválido. Intente nuevamente.")
        opc = pedir_texto_no_vacio("Ingrese el número del presupuesto a dar de baja: ")
    if opc == "0":
        print("Operación cancelada. No se realizaron cambios.")
        return
    idx = int(opc) - 1

    if not EstadoP[idx]:
        print(f"El presupuesto '{NombreP[idx]}' ya se encuentra en estado INACTIVO.")
        reactivar = pedir_texto_no_vacio("¿Desea reactivarlo? (s/n): ").lower()
        if reactivar == 's':
            EstadoP[idx] = True
            print(f"¡Presupuesto '{NombreP[idx]}' reactivado (Activo) correctamente!\n")
        else:
            print("Operación cancelada.\n")
        return

    confirmacion = pedir_texto_no_vacio(f"¿Está seguro de dar de baja el presupuesto '{NombreP[idx]}' de ${MontoP[idx]}? (s/n): ").lower()
    if confirmacion == 's':
        EstadoP[idx] = False
        print(f"¡Presupuesto '{NombreP[idx]}' dado de baja correctamente (Estado: Inactivo)!\n")
    else:
        print("Operación cancelada.\n")
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
            mostrar_gastos()
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


def menu_presupuestos(matrizP, encabezadoP):
    menu = 1
    while menu == 1:
        print("\n========================================")
        print("       GESTIÓN DE PRESUPUESTOS          ")
        print("========================================")
        print("1. Mostrar matriz")
        print("2. Consultar / Buscar presupuesto")
        print("3. Agregar nuevo presupuesto (Crear)")
        print("4. Modificar un presupuesto (Actualizar)")
        print("5. Dar de baja lógica un presupuesto")
        print("0. Volver al menú principal")
        print("========================================")
        opc = input("Seleccione una opción: ").strip()

        if opc == "1":
            obtener_matriz(presupuestos)
            mostrar_presupuestos()
        elif opc == "2":
            consultar_presupuesto()
        elif opc == "3":
            agregar_presupuesto()
        elif opc == "4":
            modificar_presupuesto()
        elif opc == "5":
            eliminar_presupuesto()
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
            obtener_matriz(gastos)
            obtener_matriz(presupuestos)
            mostrar_gastos()
            mostrar_presupuestos()
        elif opcion == "0":
            print("¡Gracias por utilizar el sistema! Hasta luego.")
            menu = 0
        else:
            print("Opción no válida. Por favor, intente nuevamente.\n")

if __name__ == "__main__":

    matrizG = obtener_matriz(gastos)
    matrizP = obtener_matriz(presupuestos)

    menu_principal(matrizG, encabezadosG, matrizP, encabezadosP)