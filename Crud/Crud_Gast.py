from Func.Auxiliares import *
from Func.Func_Matriz import *
#villereada para resolver y que funcione (fixear las funciones y el paasaje de datos)
from Datos.Datos import gastos

# Hacer buenas practicas
# Fixear las funciones 

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
        if busqueda_lower in NombreG[i].lower() or busqueda_lower in NombreC[i].lower():
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
            matriz_res.append([idx + 1, NombreG[idx], MontoG[idx], FechaG[idx], NombreC[idx], DescripcionG[idx], est])
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
    NombreC.append(categoria)
    DescripcionG.append(descripcion)
    EstadoG.append("activo")
    # RESOLVER VILLEREADA
    Periodo_Presupuesto.append("whatever")
    Id_CatGasto.append(len(Id_CatGasto))
    Id_PresGasto.append(len(Id_PresGasto))
    print("¡Gasto agregado exitosamente (Estado: Activo)!\n")
    input("Presione ENTER para continuar...")
    print(gastos[1])

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
    NombreC[idx] = pedir_opcional("Nueva categoría", NombreC[idx])
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