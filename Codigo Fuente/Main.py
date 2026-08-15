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

# CREACION Y LLENADO DINÁMICO DE MATRICES
def llenar_matrizGastos(matriz):
    filas = len(matriz)
    columnas = len(matriz[0]) 
    for fil in range(filas):
        for col in range(columnas):
            if col == 0:
                matriz[fil][col] = NombreG[fil]
            elif col == 1:
                matriz[fil][col] = MontoG[fil]
            elif col == 2:
                matriz[fil][col] = FechaG[fil]
            elif col == 3:
                matriz[fil][col] = CategoriaG[fil]
            elif col == 4:
                matriz[fil][col] = DescripcionG[fil]
            elif col == 5:
                matriz[fil][col] = "Activo" if EstadoG[fil] else "Inactivo"

def llenar_matrizPresupuestos(matriz):
    filas = len(matriz)
    columnas = len(matriz[0]) 
    for fil in range(filas):
        for col in range(columnas):
            if col == 0:
                matriz[fil][col] = NombreP[fil]
            elif col == 1:
                matriz[fil][col] = MontoP[fil]
            elif col == 2:
                matriz[fil][col] = FechaP[fil]
            elif col == 3:
                matriz[fil][col] = CategoriaP[fil]
            elif col == 4:
                matriz[fil][col] = DescripcionP[fil]
            elif col == 5:
                matriz[fil][col] = "Activo" if EstadoP[fil] else "Inactivo"

def obtener_matriz_gastos():
    cant_filas = len(NombreG)
    cant_columnas = 6
    if cant_filas == 0:
        return []
    matriz = [[0] * cant_columnas for _ in range(cant_filas)]
    llenar_matrizGastos(matriz)
    return matriz

def obtener_matriz_presupuestos():
    cant_filas = len(NombreP)
    cant_columnas = 6
    if cant_filas == 0:
        return []
    matriz = [[0] * cant_columnas for _ in range(cant_filas)]
    llenar_matrizPresupuestos(matriz)
    return matriz

# MOSTRAR MATRICES
def mostrar_matriz(encabezados, matriz):
    if not matriz:
        print("No hay datos cargados.")
        return

    filas = len(matriz)
    columnas = len(matriz[0])
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

# INGRESO Y VALIDACIÓN DE DATOS
def pedir_monto(mensaje):
    while True:
        try:
            monto = float(input(mensaje))
            if monto <= 0:
                print("El monto debe ser un número mayor a cero.")
            else:
                return monto
        except ValueError:
            print("Entrada inválida. Debe ingresar un número válido.")

def pedir_texto_no_vacio(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("Este campo no puede estar vacío.")

def pedir_opcional(mensaje, valor_actual):
    nuevo_valor = input(f"{mensaje} [{valor_actual}]: ").strip()
    if nuevo_valor == "":
        return valor_actual
    return nuevo_valor

# -----------------------------------------------------------------------------------
# CRUD: GASTOS
# -----------------------------------------------------------------------------------
def listar_gastos_numerados():
    if not NombreG:
        print("No hay gastos registrados.")
        return False
    print("\nLISTADO DE GASTOS:")
    for i in range(len(NombreG)):
        est = "Activo" if EstadoG[i] else "Inactivo"
        print(f"{i + 1}. {NombreG[i]} | Monto: ${MontoG[i]} | Cat: {CategoriaG[i]} | Fecha: {FechaG[i]} | Estado: {est}")
    return True

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

def consultar_gasto():
    print("\n--- [R] CONSULTAR / BUSCAR GASTOS ---")
    if not NombreG:
        print("No hay gastos para consultar.")
        return

    busqueda_str = pedir_texto_no_vacio("Ingrese término de búsqueda (nombre, categoría o N° de fila): ")
    busqueda_lower = busqueda_str.lower()
    coincidencias = []

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

    if not coincidencias:
        print("No se encontraron gastos que coincidan con la búsqueda.")
    else:
        print(f"\nSe encontraron {len(coincidencias)} resultado(s):")
        encabezados = ["#", "Gasto", "Monto", "Fecha", "Categoría", "Descripción", "Estado"]
        matriz_res = []
        for idx in coincidencias:
            est = "Activo" if EstadoG[idx] else "Inactivo"
            matriz_res.append([idx + 1, NombreG[idx], MontoG[idx], FechaG[idx], CategoriaG[idx], DescripcionG[idx], est])
        mostrar_matriz(encabezados, matriz_res)

def modificar_gasto():
    print("\n--- [U] MODIFICAR GASTO ---")
    if not listar_gastos_numerados():
        return

    while True:
        try:
            opc = int(input("\nSeleccione el número de gasto a modificar (0 para cancelar): "))
            if opc == 0:
                return
            if 1 <= opc <= len(NombreG):
                idx = opc - 1
                break
            print("Número fuera de rango. Intente nuevamente.")
        except ValueError:
            print("Debe ingresar un número entero válido.")

    print(f"\nModificando gasto #{opc} (Presione ENTER para conservar el valor actual):")
    NombreG[idx] = pedir_opcional("Nuevo nombre", NombreG[idx])
    
    nuevo_monto_str = input(f"Nuevo monto [${MontoG[idx]}]: ").strip()
    if nuevo_monto_str != "":
        while True:
            try:
                monto = float(nuevo_monto_str)
                if monto > 0:
                    MontoG[idx] = monto
                    break
                print("El monto debe ser un número positivo.")
            except ValueError:
                print("Entrada inválida.")
            nuevo_monto_str = input("Ingrese nuevo monto válido: ").strip()

    FechaG[idx] = pedir_opcional("Nueva fecha (DD/MM/AAAA)", FechaG[idx])
    CategoriaG[idx] = pedir_opcional("Nueva categoría", CategoriaG[idx])
    DescripcionG[idx] = pedir_opcional("Nueva descripción", DescripcionG[idx])

    estado_actual = "Activo" if EstadoG[idx] else "Inactivo"
    cambiar_est = input(f"¿Desea cambiar el estado actual ({estado_actual})? (s/n): ").strip().lower()
    if cambiar_est == 's':
        EstadoG[idx] = not EstadoG[idx]
        nuevo_est = "Activo" if EstadoG[idx] else "Inactivo"
        print(f"Estado cambiado a: {nuevo_est}")

    print("¡Gasto actualizado exitosamente!\n")

def eliminar_gasto():
    print("\n--- [D] DAR DE BAJA LÓGICA GASTO ---")
    if not listar_gastos_numerados():
        return

    while True:
        try:
            opc = int(input("\nSeleccione el número de gasto a dar de baja (0 para cancelar): "))
            if opc == 0:
                return
            if 1 <= opc <= len(NombreG):
                idx = opc - 1
                break
            print("Número fuera de rango. Intente nuevamente.")
        except ValueError:
            print("Debe ingresar un número entero válido.")

    if not EstadoG[idx]:
        print(f"El gasto '{NombreG[idx]}' ya se encuentra en estado INACTIVO.")
        reactivar = input("¿Desea reactivarlo? (s/n): ").strip().lower()
        if reactivar == 's':
            EstadoG[idx] = True
            print(f"¡Gasto '{NombreG[idx]}' reactivado (Activo) correctamente!\n")
        else:
            print("Operación cancelada.\n")
        return

    confirmacion = input(f"¿Está seguro de dar de baja el gasto '{NombreG[idx]}' de ${MontoG[idx]}? (s/n): ").strip().lower()
    if confirmacion == 's':
        EstadoG[idx] = False
        print(f"¡Gasto '{NombreG[idx]}' dado de baja correctamente (Estado: Inactivo)!\n")
    else:
        print("Operación cancelada.\n")

# -----------------------------------------------------------------------------------
# CRUD: PRESUPUESTOS
# -----------------------------------------------------------------------------------
def listar_presupuestos_numerados():
    if not NombreP:
        print("No hay presupuestos registrados.")
        return False
    print("\nLISTADO DE PRESUPUESTOS:")
    for i in range(len(NombreP)):
        est = "Activo" if EstadoP[i] else "Inactivo"
        print(f"{i + 1}. {NombreP[i]} | Límite: ${MontoP[i]} | Cat: {CategoriaP[i]} | Fecha: {FechaP[i]} | Estado: {est}")
    return True

def agregar_presupuesto():
    print("\n--- [C] AGREGAR NUEVO PRESUPUESTO ---")
    nombre = pedir_texto_no_vacio("Ingrese nombre del presupuesto: ")
    monto = pedir_monto("Ingrese monto límite: ")
    fecha = pedir_texto_no_vacio("Ingrese fecha (DD/MM/AAAA): ")
    categoria = pedir_texto_no_vacio("Ingrese categoría: ")
    descripcion = pedir_texto_no_vacio("Ingrese descripción: ")

    NombreP.append(nombre)
    MontoP.append(monto)
    FechaP.append(fecha)
    CategoriaP.append(categoria)
    DescripcionP.append(descripcion)
    EstadoP.append(True)
    print("¡Presupuesto agregado exitosamente (Estado: Activo)!\n")

def consultar_presupuesto():
    print("\n--- [R] CONSULTAR / BUSCAR PRESUPUESTOS ---")
    if not NombreP:
        print("No hay presupuestos para consultar.")
        return

    busqueda_str = pedir_texto_no_vacio("Ingrese término de búsqueda (nombre, categoría o N° de fila): ")
    busqueda_lower = busqueda_str.lower()
    coincidencias = []

    # Búsqueda por número de fila (1..N)
    if busqueda_str.isdigit():
        num = int(busqueda_str)
        if 1 <= num <= len(NombreP):
            coincidencias.append(num - 1)

    # Búsqueda por texto (nombre o categoría)
    for i in range(len(NombreP)):
        if busqueda_lower in NombreP[i].lower() or busqueda_lower in CategoriaP[i].lower():
            if i not in coincidencias:
                coincidencias.append(i)

    if not coincidencias:
        print("No se encontraron presupuestos que coincidan con la búsqueda.")
    else:
        print(f"\nSe encontraron {len(coincidencias)} resultado(s):")
        encabezados = ["#", "Presupuesto", "Monto Límite", "Fecha", "Categoría", "Descripción", "Estado"]
        matriz_res = []
        for idx in coincidencias:
            est = "Activo" if EstadoP[idx] else "Inactivo"
            matriz_res.append([idx + 1, NombreP[idx], MontoP[idx], FechaP[idx], CategoriaP[idx], DescripcionP[idx], est])
        mostrar_matriz(encabezados, matriz_res)

def modificar_presupuesto():
    print("\n--- [U] MODIFICAR PRESUPUESTO ---")
    if not listar_presupuestos_numerados():
        return

    while True:
        try:
            opc = int(input("\nSeleccione el número de presupuesto a modificar (0 para cancelar): "))
            if opc == 0:
                return
            if 1 <= opc <= len(NombreP):
                idx = opc - 1
                break
            print("Número fuera de rango. Intente nuevamente.")
        except ValueError:
            print("Debe ingresar un número entero válido.")

    print(f"\nModificando presupuesto #{opc} (Presione ENTER para conservar el valor actual):")
    NombreP[idx] = pedir_opcional("Nuevo nombre", NombreP[idx])
    
    nuevo_monto_str = input(f"Nuevo monto límite [${MontoP[idx]}]: ").strip()
    if nuevo_monto_str != "":
        while True:
            try:
                monto = float(nuevo_monto_str)
                if monto > 0:
                    MontoP[idx] = monto
                    break
                print("El monto debe ser un número positivo.")
            except ValueError:
                print("Entrada inválida.")
            nuevo_monto_str = input("Ingrese nuevo monto límite válido: ").strip()

    FechaP[idx] = pedir_opcional("Nueva fecha (DD/MM/AAAA)", FechaP[idx])
    CategoriaP[idx] = pedir_opcional("Nueva categoría", CategoriaP[idx])
    DescripcionP[idx] = pedir_opcional("Nueva descripción", DescripcionP[idx])

    estado_actual = "Activo" if EstadoP[idx] else "Inactivo"
    cambiar_est = input(f"¿Desea cambiar el estado actual ({estado_actual})? (s/n): ").strip().lower()
    if cambiar_est == 's':
        EstadoP[idx] = not EstadoP[idx]
        nuevo_est = "Activo" if EstadoP[idx] else "Inactivo"
        print(f"Estado cambiado a: {nuevo_est}")

    print("¡Presupuesto actualizado exitosamente!\n")

def eliminar_presupuesto():
    print("\n--- [D] DAR DE BAJA LÓGICA PRESUPUESTO ---")
    if not listar_presupuestos_numerados():
        return

    while True:
        try:
            opc = int(input("\nSeleccione el número de presupuesto a dar de baja (0 para cancelar): "))
            if opc == 0:
                return
            if 1 <= opc <= len(NombreP):
                idx = opc - 1
                break
            print("Número fuera de rango. Intente nuevamente.")
        except ValueError:
            print("Debe ingresar un número entero válido.")

    if not EstadoP[idx]:
        print(f"El presupuesto '{NombreP[idx]}' ya se encuentra en estado INACTIVO.")
        reactivar = input("¿Desea reactivarlo? (s/n): ").strip().lower()
        if reactivar == 's':
            EstadoP[idx] = True
            print(f"¡Presupuesto '{NombreP[idx]}' reactivado (Activo) correctamente!\n")
        else:
            print("Operación cancelada.\n")
        return

    confirmacion = input(f"¿Está seguro de dar de baja el presupuesto '{NombreP[idx]}' de ${MontoP[idx]}? (s/n): ").strip().lower()
    if confirmacion == 's':
        EstadoP[idx] = False
        print(f"¡Presupuesto '{NombreP[idx]}' dado de baja correctamente (Estado: Inactivo)!\n")
    else:
        print("Operación cancelada.\n")

# -----------------------------------------------------------------------------------
# MENÚS DE NAVEGACIÓN
# -----------------------------------------------------------------------------------
def ver_tablas_completas():
    encabezadosG = ["Gastos", "Monto", "Fecha", "Categoria", "Descripcion", "Estado"]
    encabezadosP = ["Presupuestos", "Monto Límite", "Fecha", "Categoria", "Descripcion", "Estado"]

    print("\n=================== MATRIZ DE GASTOS ===================")
    matriz_g = obtener_matriz_gastos()
    mostrar_matriz(encabezadosG, matriz_g)
    print()

    print("================ MATRIZ DE PRESUPUESTOS ================")
    matriz_p = obtener_matriz_presupuestos()
    mostrar_matriz(encabezadosP, matriz_p)
    print()

def menu_gastos():
    while True:
        print("\n========================================")
        print("         GESTIÓN DE GASTOS              ")
        print("========================================")
        print("1. Listar todos los gastos")
        print("2. Consultar / Buscar gasto")
        print("3. Agregar nuevo gasto (Crear)")
        print("4. Modificar un gasto (Actualizar)")
        print("5. Dar de baja lógica un gasto")
        print("0. Volver al menú principal")
        print("========================================")
        opc = input("Seleccione una opción: ").strip()

        if opc == "1":
            listar_gastos_numerados()
        elif opc == "2":
            consultar_gasto()
        elif opc == "3":
            agregar_gasto()
        elif opc == "4":
            modificar_gasto()
        elif opc == "5":
            eliminar_gasto()
        elif opc == "0":
            break
        else:
            print("Opción no válida. Intente nuevamente.")

def menu_presupuestos():
    while True:
        print("\n========================================")
        print("       GESTIÓN DE PRESUPUESTOS          ")
        print("========================================")
        print("1. Listar todos los presupuestos")
        print("2. Consultar / Buscar presupuesto")
        print("3. Agregar nuevo presupuesto (Crear)")
        print("4. Modificar un presupuesto (Actualizar)")
        print("5. Dar de baja lógica un presupuesto")
        print("0. Volver al menú principal")
        print("========================================")
        opc = input("Seleccione una opción: ").strip()

        if opc == "1":
            listar_presupuestos_numerados()
        elif opc == "2":
            consultar_presupuesto()
        elif opc == "3":
            agregar_presupuesto()
        elif opc == "4":
            modificar_presupuesto()
        elif opc == "5":
            eliminar_presupuesto()
        elif opc == "0":
            break
        else:
            print("Opción no válida. Intente nuevamente.")

def menu_principal():
    while True:
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
            menu_gastos()
        elif opcion == "2":
            menu_presupuestos()
        elif opcion == "3":
            ver_tablas_completas()
        elif opcion == "0":
            print("¡Gracias por utilizar el sistema! Hasta luego.")
            break
        else:
            print("Opción no válida. Por favor, intente nuevamente.\n")

if __name__ == "__main__":
    menu_principal()


