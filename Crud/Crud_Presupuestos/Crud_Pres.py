import os
from Func.Func_Rich import console, mostrar_mensaje, renderizar_tabla
from Func.Func_val import (
    pedir_monto,
    pedir_monto_opcional,
    solicitar_y_verificar_fecha,
    pedir_texto_no_vacio,
    pedir_opcional,
    pedir_opcion_menu,
    seleccionar_categoria_id
)
from Func.Func_Matriz import obtener_nombre_categoria, fila_a_diccionario
from rich.table import Table
from Datos.Datos import(
    categoria_ruta,
    presupuesto_ruta,
    encabezadosP
)



def mostrar_presupuestos(archivo=presupuesto_ruta,encabezados=encabezadosP):
    console.print("\n[bold cyan]--- LISTADO DE PRESUPUESTOS ---[/bold cyan]")
    filas = []
    try:
        with open(archivo, "r", encoding="utf-8") as arch:
            for linea in arch:
                datos = linea.strip().split("|")
                filas.append(datos)
    except FileNotFoundError:
        mostrar_mensaje("El archivo no existe.", "error")

    renderizar_tabla(encabezados, filas, "Listado de Presupuestos")
    console.input("\n[dim]Presione ENTER para continuar...[/dim]")

def modificar_presupuesto(archivo=presupuesto_ruta, archivo_cat=categoria_ruta):
    console.print("\n[bold blue]--- [U] MODIFICAR PRESUPUESTO ---[/bold blue]")

    try:
        with open(archivo, "r", encoding="utf-8") as arch:
            presupuestos = [linea.strip().split("|") for linea in arch if linea.strip()]

        with open(archivo_cat, "r", encoding="utf-8") as arch:
            categorias = [linea.strip().split("|") for linea in arch if linea.strip()]

    except FileNotFoundError:
        mostrar_mensaje("No se encontró alguno de los archivos.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    activas = [p for p in presupuestos if p[4] == "Activo"]

    if not activas:
        mostrar_mensaje("No hay presupuestos activos para modificar.", "alerta")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    console.print("Seleccione el presupuesto a modificar:")

    for i in range(len(activas)):
        p = activas[i]
        nom_c = obtener_nombre_categoria(p[1], categorias)

        console.print(
            f"  [yellow]{i + 1}[/yellow]. ID {p[0]} - {nom_c} "
            f"| Período: {p[2]} | Límite: ${float(p[3]):,.2f}"
        )

    opciones = [str(i + 1) for i in range(len(activas))]
    opciones.append("0")

    opc = pedir_opcion_menu(
        "Seleccione opción (0 para cancelar):", opciones
    )

    if opc == "0":
        return

    idx = int(opc) - 1
    p_sel = activas[idx]

    console.print("\n[dim]Presione ENTER para conservar los valores actuales:[/dim]")

    p_sel[2] = pedir_opcional(
        "Nuevo período (DD/MM/AAAA-DD/MM/AAAA)", p_sel[2]
    )

    p_sel[3] = str(pedir_monto_opcional(
        "Nuevo monto límite", float(p_sel[3])
    ))

    cambiar_cat = pedir_texto_no_vacio(
        "¿Desea reasignar la categoría asociada? (s/n):"
    ).lower()

    if cambiar_cat == "s":
        nuevo_id_cat = seleccionar_categoria_id(categorias)

        if nuevo_id_cat:
            p_sel[1] = nuevo_id_cat

    cambiar_est = pedir_texto_no_vacio(
        f"¿Cambiar estado actual ({p_sel[4]})? (s/n):"
    ).lower()

    if cambiar_est == "s":
        p_sel[4] = "Inactivo" if p_sel[4] == "Activo" else "Activo"
        mostrar_mensaje(f"Estado cambiado a: {p_sel[4]}", "info")

    try:
        with open(archivo, "w", encoding="utf-8") as arch:
            for p in presupuestos:
                arch.write("|".join(map(str, p)) + "\n")

        mostrar_mensaje("Presupuesto actualizado exitosamente.", "exito")

    except OSError as error:
        mostrar_mensaje(f"Error al guardar el presupuesto: {error}", "error")

    console.input("[dim]Presione ENTER para continuar...[/dim]")

def eliminar_presupuesto(archivo=presupuesto_ruta, archivo_cat=categoria_ruta):
    console.print("\n[bold red]--- [D] BAJA / REACTIVACIÓN LÓGICA DE PRESUPUESTO ---[/bold red]")

    try:
        with open(archivo, "r", encoding="utf-8") as arch:
            presupuestos = [linea.strip().split("|") for linea in arch if linea.strip()]

        with open(archivo_cat, "r", encoding="utf-8") as arch:
            categorias = [linea.strip().split("|") for linea in arch if linea.strip()]

    except FileNotFoundError:
        mostrar_mensaje("No se encontró alguno de los archivos.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    if not presupuestos:
        mostrar_mensaje("No hay presupuestos registrados.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    for i in range(len(presupuestos)):
        p = presupuestos[i]
        nom_c = obtener_nombre_categoria(p[1], categorias)
        col_est = "green" if p[4] == "Activo" else "red"

        console.print(
            f"  [yellow]{i + 1}[/yellow]. ID {p[0]} - {nom_c} "
            f"| Límite: ${float(p[3]):,.2f} "
            f"[{col_est}]({p[4]})[/{col_est}]"
        )

    opciones = [str(i + 1) for i in range(len(presupuestos))]
    opciones.append("0")

    opc = pedir_opcion_menu(
        "Seleccione el presupuesto (0 para cancelar):", opciones
    )

    if opc == "0":
        return

    idx = int(opc) - 1
    p = presupuestos[idx]
    nom_c = obtener_nombre_categoria(p[1], categorias)

    if p[4] == "Inactivo":
        reactivar = pedir_texto_no_vacio(
            f"El presupuesto de '{nom_c}' está INACTIVO. ¿Desea reactivarlo? (s/n):"
        ).lower()

        if reactivar == "s":
            p[4] = "Activo"
            mensaje = "Presupuesto reactivado correctamente."
            tipo = "exito"
        else:
            mensaje = "Operación cancelada."
            tipo = "info"

    else:
        confirmar = pedir_texto_no_vacio(
            f"¿Confirmar baja lógica del presupuesto para '{nom_c}'? (s/n):"
        ).lower()

        if confirmar == "s":
            p[4] = "Inactivo"
            mensaje = "Presupuesto dado de baja correctamente (Inactivo)."
            tipo = "exito"
        else:
            mensaje = "Operación cancelada."
            tipo = "info"

    if tipo == "exito":

        temp = os.path.join(os.path.dirname(archivo), "temp.txt")

        try:
            with open(temp, "w", encoding="utf-8") as arch:
                for p in presupuestos:
                    arch.write("|".join(p) + "\n")

            os.replace(temp, archivo)

        except OSError as error:
            mostrar_mensaje(f"Error al guardar los cambios: {error}", "error")

            if os.path.exists(temp):
                os.remove(temp)

            console.input("[dim]Presione ENTER para continuar...[/dim]")
            return

    mostrar_mensaje(mensaje, tipo)
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def agregar_presupuesto(archivo=presupuesto_ruta, archivo_cat=categoria_ruta):
    console.print("\n[bold green]--- [C] AGREGAR NUEVO PRESUPUESTO ---[/bold green]")

    try:
        with open(archivo, "r", encoding="utf-8") as arch:
            presupuestos = [linea.strip().split("|") for linea in arch if linea.strip()]

        with open(archivo_cat, "r", encoding="utf-8") as arch:
            categorias = [linea.strip().split("|") for linea in arch if linea.strip()]

    except FileNotFoundError:
        mostrar_mensaje("No se encontró alguno de los archivos.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    id_cat = seleccionar_categoria_id(categorias)

    if not id_cat:
        return

    for p in presupuestos:
        if p[1] == id_cat and p[4] == "Activo":
            nom_c = obtener_nombre_categoria(id_cat, categorias)

            mostrar_mensaje(
                f"Ya existe un presupuesto activo asignado a la categoría '{nom_c}'.",
                "alerta"
            )

            console.input("[dim]Presione ENTER para continuar...[/dim]")
            return

    console.print("[dim]Definición del período de vigencia:[/dim]")

    f_inicio = solicitar_y_verificar_fecha("Fecha de Inicio (DD/MM/AAAA):")
    f_fin = solicitar_y_verificar_fecha("Fecha de Cierre (DD/MM/AAAA):")

    periodo = f"{f_inicio}-{f_fin}"

    monto = pedir_monto("Ingrese monto límite mensual asignado:")

    ids_existentes = [int(p[0]) for p in presupuestos if p[0].isdigit()]
    nuevo_id = str(max(ids_existentes) + 1) if ids_existentes else "1"

    nuevo_presupuesto = [nuevo_id, id_cat, periodo, str(monto), "Activo"]

    try:
        with open(archivo, "a", encoding="utf-8") as arch:
            arch.write("|".join(nuevo_presupuesto) + "\n")

    except OSError as error:
        mostrar_mensaje(f"Error al guardar el presupuesto: {error}", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    nom_cat = obtener_nombre_categoria(id_cat, categorias)

    mostrar_mensaje(
        f"Presupuesto para '{nom_cat}' creado con éxito "
        f"(ID: {nuevo_id}, Límite: ${float(monto):,.2f}).",
        "exito"
    )

    console.input("[dim]Presione ENTER para continuar...[/dim]")

def buscar_presupuesto(archivo=presupuesto_ruta):

    console.print("\n[bold yellow]--- BUSCAR PRESUPUESTO POR ID ---[/bold yellow]")
    busqueda = pedir_texto_no_vacio("Ingrese el ID del presupuesto:").strip().lower()
    encontrado = False

    try:
        arch = open(archivo, "r", encoding="UTF-8")
        linea = arch.readline()
        while linea and not encontrado:
            linea = linea.strip()
            if linea:
                try:
                    id_p, id_cat, periodo, limite, estado = linea.split("|")
                    if id_p.lower() == busqueda:
                        encontrado = True
                        console.print(f'\n{"ID":6}{"Categoría":12}{"Período":12}{"Límite":14}{"Estado":10}')
                        console.print(f'{id_p:6}{id_cat:12}{periodo:12}{float(limite):<14,.2f}{estado:10}')
                except ValueError:
                    mostrar_mensaje(f"Línea con formato inválido, se omite: {linea}", "alerta")
            linea = arch.readline()
        if not encontrado:
            mostrar_mensaje("No se encontró ningún presupuesto con ese ID.", "alerta")
    except OSError:
        mostrar_mensaje("No se pudo leer el archivo de presupuestos.", "error")
    finally:
        try:
            arch.close()
        except:
            print("No se pudo cerrar el archivo")
    console.input("[dim]Presione ENTER para continuar...[/dim]")