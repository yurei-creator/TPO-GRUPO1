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
        for col in range(columnas):
            valor = str(matriz[fila][col])
            espacios = " " * (anchos[col] - len(valor))
            print(valor + espacios + "  ", end="")  
        print()
    print()  # Línea en blanco después de la matriz
# INGRESO Y VALIDACIÓN DE DATOS
def pedir_monto(mensaje):
    dato_invalido = True
    while dato_invalido:
        numero_valido = True
        monto = input(mensaje)
        puntos_encontrados = 0
        if monto != "":
            for caracter in monto:
                if caracter == "." or caracter == ",":
                   puntos_encontrados += 1
                if caracter == ".":
                    monto_limpio += "."
                if caracter == ",":
                   monto_limpio += ","
                elif caracter < "0" or caracter > "9":
                    numero_valido = False
            if puntos_encontrados > 1:
                numero_valido = False
            if numero_valido:
                monto_final = float(monto_limpio)
                if monto_final > 0:
                    dato_invalido = False
                    return monto_final
                else: 
                    print("El monto debe ser un número mayor a cero.")
            else:
                print("Error: el formato introducido no es un numero valido")
        else:
            print("El campo no puede estar vacío.")
def validar_fecha(fecha):
    pass
def pedir_texto_no_vacio(mensaje):
    text = False
    while not text:
        texto = input(mensaje)
        if texto != "":
            for caracter in texto:
                if caracter != " ":
                    texto += caracter
                text = True
                print("DEBUG [INFO]: Se ingresó el texto: " + texto)
                return texto
        else:
            print("[AVISO]: Este campo no puede estar vacío.")

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
    if busqueda_str.isdigit():
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
    nombre = pedir_texto_no_vacio("Ingrese nombre del gasto: ")
    monto = pedir_monto("Ingrese monto: ")
    fecha = pedir_texto_no_vacio("Ingrese fecha (DD/MM/AAAA): ")
    categoria = pedir_texto_no_vacio("Ingrese categoría: ")
    descripcion = pedir_texto_no_vacio("Ingrese descripción: ")

    NombreG.append(nombre)
    MontoG.append(monto)
    FechaG.append(fecha)
    CategoriaG.append(categoria)
    DescripcionG.append(descripcion)
    EstadoG.append(True)
    print("¡Gasto agregado exitosamente (Estado: Activo)!\n")

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
        opc = input("Seleccione una opción: ").strip()

        if opc == "1":
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
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            menu_gastos(matrizG, encabezadoG)
        elif opcion == "2":
            menu_presupuestos(matrizP, encabezadoP)
        elif opcion == "3":
            ver_tablas_completas()
        elif opcion == "0":
            print("¡Gracias por utilizar el sistema! Hasta luego.")
            menu = 0
        else:
            print("Opción no válida. Por favor, intente nuevamente.\n")

if __name__ == "__main__":

    matrizG = obtener_matriz(gastos)
    matrizP = obtener_matriz(presupuestos)

    menu_principal(matrizG, encabezadosG, matrizP, encabezadosP)