import os
from Func.Func_Rich import console, mostrar_mensaje, renderizar_tabla
from Func.Func_val import pedir_texto_no_vacio, pedir_opcional, pedir_opcion_menu
from Func.Func_Matriz import fila_a_diccionario
from rich.table import Table
from Datos.Datos import categoria_ruta, encabezadosC


def obtener_ultimo_codigo(archivo=categoria_ruta):
    ultimo_codigo = "1"
    nombres = []

    try:
        arch = open(archivo, "r", encoding="UTF-8")

        for linea in arch:
            fila = linea.strip().split("|")

            ultimo_codigo = int(fila[0])
            nombres.append(fila[1].lower())

        arch.close()

    except OSError as mensaje:
        print("No se puede leer el archivo:", mensaje)

    return ultimo_codigo, nombres

def alta_categoria(archivo=categoria_ruta):
    ultimo, nombres = obtener_ultimo_codigo()
    nuevo_codigo = int(ultimo) + 1


    nombre = pedir_texto_no_vacio("Ingrese nombre de la categoría:")

    while nombre.lower() in nombres:
        nombre = pedir_texto_no_vacio("Esa categoria ya existe, ingrese un nuevo nombre:")
    descripcion = pedir_texto_no_vacio("Ingrese descripción:")
    estado = "Activo"
    
    try:
        arch = open(archivo, "a", encoding="UTF-8")
        nueva_categoria = f'{nuevo_codigo}|{nombre}|{descripcion}|{estado}\n'
        arch.write(nueva_categoria)
        mostrar_mensaje(f"Categoría '{nombre}' agregada exitosamente con ID: {nuevo_codigo}", "exito")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
    except OSError as mensaje:
        print("No se puede grabar el archivo:", mensaje)
    finally:
        try:
            arch.close()
        except NameError:
            pass

def eliminar_categoria(archivo=categoria_ruta):
    console.print("\n[bold red]--- [D] BAJA / REACTIVACIÓN LÓGICA DE CATEGORÍA ---[/bold red]")

    try:
        with open(archivo, "r", encoding="utf-8") as f:
            categoria = [linea.strip().split("|") for linea in f if linea.strip()]

    except FileNotFoundError:
        mostrar_mensaje("No se encontró el archivo de categorías.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    if not categoria:
        mostrar_mensaje("No hay categorías registradas.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    console.print("Listado general de categorías:")

    for i in range(len(categoria)):
        c = categoria[i]
        color_est = "green" if c[3] == "Activo" else "red"

        console.print(
            f"  [yellow]{i + 1}[/yellow]. ID {c[0]} - {c[1]} "
            f"[{color_est}]({c[3]})[/{color_est}]"
        )

    opciones = [str(i + 1) for i in range(len(categoria))]
    opciones.append("0")

    opc = pedir_opcion_menu(
        "Seleccione el número de categoría a cambiar estado (0 para cancelar):",
        opciones
    )

    if opc == "0":
        return

    idx = int(opc) - 1
    c = categoria[idx]

    if c[3] == "Inactivo":
        reactivar = pedir_texto_no_vacio(
            f"La categoría '{c[1]}' está INACTIVA. ¿Desea reactivarla? (s/n):"
        ).lower()

        if reactivar == "s":
            c[3] = "Activo"
            mensaje = f"Categoría '{c[1]}' reactivada con éxito."
            tipo = "exito"
        else:
            mensaje = "Operación cancelada."
            tipo = "info"

    else:
        confirmar = pedir_texto_no_vacio(
            f"¿Confirmar baja lógica de la categoría '{c[1]}'? (s/n):"
        ).lower()

        if confirmar == "s":
            c[3] = "Inactivo"
            mensaje = f"Categoría '{c[1]}' dada de baja correctamente (Inactivo)."
            tipo = "exito"
        else:
            mensaje = "Operación cancelada."
            tipo = "info"

    if tipo == "exito":
        with open(archivo, "w", encoding="utf-8") as f:
            for c in categoria:
                f.write("|".join(c) + "\n")

    mostrar_mensaje(mensaje, tipo)
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def modificar_categoria(archivo=categoria_ruta):
    codigo_modif = input("Ingrese el código de la categoría a modificar: ")
    temp = "temp.txt"
    encontrado = False

    try:
        with open(archivo, "rt", encoding="utf-8") as arch, \
             open(temp, "wt", encoding="utf-8") as aux:

            for linea in arch:
                datos = linea.strip().split("|")

                codigo = datos[0]

                if codigo == codigo_modif:
                    encontrado = True

                    nombre = datos[1]
                    descripcion = datos[2]
                    estado = datos[3]

                    print(f"\nCategoría encontrada: {codigo} - {nombre} - {descripcion}")

                    nuevo_nombre = input(
                        "Nuevo nombre (Enter para mantener): "
                    ).strip()

                    if nuevo_nombre == "":
                        nuevo_nombre = nombre

                    nueva_descripcion = input(
                        "Nueva descripción (Enter para mantener): "
                    ).strip()

                    if nueva_descripcion == "":
                        nueva_descripcion = descripcion

                    nueva_linea = f"{codigo}|{nuevo_nombre}|{nueva_descripcion}|{estado}\n"

                    aux.write(nueva_linea)

                    print(f"Categoría {codigo} modificada.")

                else:
                    aux.write(linea)

    except FileNotFoundError:
        print("El archivo no existe.")
        return

    except OSError as error:
        print("Error en el acceso al archivo:", error)
        return

    if encontrado:
        try:
            os.replace(temp, archivo)
        except OSError as error:
            print("Error al reemplazar el archivo:", error)

    else:
        os.remove(temp)
        print(f"No se encontró la categoría {codigo_modif}.")

def mostrar_categorias(archivo=categoria_ruta,encabezados=encabezadosC):
    console.print("\n[bold cyan]--- LISTADO DE PRESUPUESTOS ---[/bold cyan]")
    filas = []
    try:
        with open(archivo, "r", encoding="utf-8") as arch:
            for linea in arch:
                datos = linea.strip().split("|")
                filas.append(datos)
    except FileNotFoundError:
        mostrar_mensaje("El archivo no existe.", "error")

    renderizar_tabla(encabezados, filas, "Listado de Categorías")
    console.input("\n[dim]Presione ENTER para continuar...[/dim]")
