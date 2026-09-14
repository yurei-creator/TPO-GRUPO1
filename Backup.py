# HAY QUE RENOMBRAR ESTE A MAIN

# Funciones Rich
from Func.Func_Rich import *
from Func.Auxiliares import *
from Func.Func_Matriz import *
from Menus.menus import *
from Crud.Crud_Gast import *

# -- FUNCIONES RICH

# Desde Func.Func_Rich

# --FUNCIONES DE VALIDACION

# Desde Func.Auxiliares

# -- FUNCIONES MATRICES

# Desde Func.Func_Matriz 

# CRUD CATEGORIAS

def agregar_categoria():
    console.print("\n[bold green]--- [C] AGREGAR NUEVA CATEGORÍA ---[/bold green]")
    nuevo_id = str(len(Id_Categoria) + 1)
    nombre = pedir_texto_no_vacio("Ingrese nombre de la categoría: ")
    descripcion = pedir_texto_no_vacio("Ingrese descripción: ")

    Id_Categoria.append(nuevo_id)
    NombreC.append(nombre)
    DescripcionC.append(descripcion)
    EstadoC.append("Activo")
    mostrar_mensaje(f"Categoría '{nombre}' agregada con ID: {nuevo_id}", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")


def consultar_categoria():
    console.print("\n[bold yellow]--- [R] CONSULTAR / BUSCAR CATEGORÍAS ---[/bold yellow]")
    if not Id_Categoria:
        mostrar_mensaje("No hay categorías registradas.", "error")
        return

    busqueda = pedir_texto_no_vacio("Ingrese término de búsqueda (ID o Nombre): ").lower()
    coincidencias = []

    for i in range(len(Id_Categoria)):
        if busqueda == Id_Categoria[i].lower() or busqueda in NombreC[i].lower():
            coincidencias.append(i)

    if not coincidencias:
        mostrar_mensaje("No se encontraron coincidencias.", "alerta")
    else:
        tabla = Table(title=f"Resultados para '{busqueda}'", header_style="bold magenta")
        for enc in encabezadosC:
            tabla.add_column(enc)
        tabla.add_column("Estado")

        for idx in coincidencias:
            tabla.add_row(Id_Categoria[idx], NombreC[idx], DescripcionC[idx], EstadoC[idx])
        console.print(tabla)
        console.input("[dim]Presione ENTER para continuar...[/dim]")


def modificar_categoria():
    console.print("\n[bold blue]--- [U] MODIFICAR CATEGORÍA ---[/bold blue]")
    id_cat = seleccionar_categoria()
    if id_cat == "0":
        return

    idx = -1
    for i in range(len(Id_Categoria)):
        if Id_Categoria[i] == id_cat:
            idx = i

    if idx == -1:
        mostrar_mensaje("ID no encontrado.", "error")
        return

    NombreC[idx] = pedir_opcional("Nuevo nombre", NombreC[idx])
    DescripcionC[idx] = pedir_opcional("Nueva descripción", DescripcionC[idx])

    cambiar_est = pedir_texto_no_vacio(f"¿Cambiar estado actual ({EstadoC[idx]})? (s/n): ").lower()
    if cambiar_est == "s":
        EstadoC[idx] = "Inactivo" if EstadoC[idx] == "Activo" else "Activo"
        mostrar_mensaje(f"Estado cambiado a: {EstadoC[idx]}", "info")

    mostrar_mensaje("Categoría actualizada exitosamente.", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")


def eliminar_categoria():
    console.print("\n[bold red]--- [D] BAJA LÓGICA DE CATEGORÍA ---[/bold red]")
    id_cat = seleccionar_categoria()
    if id_cat == "0":
        return

    idx = -1
    for i in range(len(Id_Categoria)):
        if Id_Categoria[i] == id_cat:
            idx = i

    if idx == -1:
        mostrar_mensaje("ID no encontrado.", "error")
        return

    if EstadoC[idx] == "Inactivo":
        reactivar = pedir_texto_no_vacio("Ya está inactiva. ¿Desea reactivarla? (s/n): ").lower()
        if reactivar == "s":
            EstadoC[idx] = "Activo"
            mostrar_mensaje("Categoría reactivada.", "exito")
        return

    confirmar = pedir_texto_no_vacio(f"¿Dar de baja la categoría '{NombreC[idx]}'? (s/n): ").lower()
    if confirmar == "s":
        EstadoC[idx] = "Inactivo"
        mostrar_mensaje("Categoría dada de baja correctamente.", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

## CRUD PRESUPUESTOS

def agregar_presupuesto():
    console.print("\n[bold green]--- [C] AGREGAR NUEVO PRESUPUESTO ---[/bold green]")
    nuevo_id = str(len(Id_Presupuesto) + 1)
    console.print("[dim]Definición de período:[/dim]")
    console.print("Fecha de Inicio:")
    f_inicio = solicitar_y_verificar_fecha()
    console.print("Fecha de Fin:")
    f_fin = solicitar_y_verificar_fecha()
    periodo = f"{f_inicio}-{f_fin}"

    monto = str(pedir_monto("Ingrese monto límite: "))
    id_cat = seleccionar_categoria()

    Id_Presupuesto.append(nuevo_id)
    Periodo_Presupuesto.append(periodo)
    Monto_limite.append(monto)
    Id_CategoriaP.append(id_cat)
    EstadoP.append("Activo")

    mostrar_mensaje(f"Presupuesto agregado con ID: {nuevo_id}", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")


def consultar_presupuesto():
    console.print("\n[bold yellow]--- [R] CONSULTAR / BUSCAR PRESUPUESTO ---[/bold yellow]")
    if not Id_Presupuesto:
        mostrar_mensaje("No hay presupuestos registrados.", "error")
        return

    busqueda = pedir_texto_no_vacio("Ingrese término de búsqueda (ID, Periodo o ID Categoría): ").lower()
    coincidencias = []

    for i in range(len(Id_Presupuesto)):
        if (busqueda == Id_Presupuesto[i].lower()
            or busqueda in Periodo_Presupuesto[i].lower()
            or busqueda == Id_CategoriaP[i].lower()):
            coincidencias.append(i)

    if not coincidencias:
        mostrar_mensaje("No se encontraron coincidencias.", "alerta")
    else:
        tabla = Table(title=f"Resultados para '{busqueda}'", header_style="bold magenta")
        for enc in encabezadosP:
            tabla.add_column(enc)
        tabla.add_column("Estado")

        for idx in coincidencias:
            tabla.add_row(
                Id_Presupuesto[idx],
                Periodo_Presupuesto[idx],
                Monto_limite[idx],
                Id_CategoriaP[idx],
                EstadoP[idx],
            )
        console.print(tabla)
        console.input("[dim]Presione ENTER para continuar...[/dim]")


def modificar_presupuesto():
    console.print("\n[bold blue]--- [U] MODIFICAR PRESUPUESTO ---[/bold blue]")
    id_p = seleccionar_presupuesto()
    if id_p == "0":
        return

    idx = -1
    for i in range(len(Id_Presupuesto)):
        if Id_Presupuesto[i] == id_p:
            idx = i

    if idx == -1:
        mostrar_mensaje("ID no encontrado.", "error")
        return

    Periodo_Presupuesto[idx] = pedir_opcional("Nuevo periodo (DD/MM/AAAA-DD/MM/AAAA)", Periodo_Presupuesto[idx])
    Monto_limite[idx] = str(pedir_monto_opcional("Nuevo monto límite", Monto_limite[idx]))
    Id_CategoriaP[idx] = pedir_opcional("Nuevo ID Categoría", Id_CategoriaP[idx])

    cambiar_est = pedir_texto_no_vacio(f"¿Cambiar estado actual ({EstadoP[idx]})? (s/n): ").lower()
    if cambiar_est == "s":
        EstadoP[idx] = "Inactivo" if EstadoP[idx] == "Activo" else "Activo"
        mostrar_mensaje(f"Estado cambiado a: {EstadoP[idx]}", "info")

    mostrar_mensaje("Presupuesto actualizado exitosamente.", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")


def eliminar_presupuesto():
    console.print("\n[bold red]--- [D] BAJA LÓGICA DE PRESUPUESTO ---[/bold red]")
    id_p = seleccionar_presupuesto()
    if id_p == "0":
        return

    idx = -1
    for i in range(len(Id_Presupuesto)):
        if Id_Presupuesto[i] == id_p:
            idx = i

    if idx == -1:
        mostrar_mensaje("ID no encontrado.", "error")
        return

    if EstadoP[idx] == "Inactivo":
        reactivar = pedir_texto_no_vacio("Ya está inactivo. ¿Desea reactivarlo? (s/n): ").lower()
        if reactivar == "s":
            EstadoP[idx] = "Activo"
            mostrar_mensaje("Presupuesto reactivado.", "exito")
        return

    confirmar = pedir_texto_no_vacio(f"¿Dar de baja el presupuesto ID '{Id_Presupuesto[idx]}'? (s/n): ").lower()
    if confirmar == "s":
        EstadoP[idx] = "Inactivo"
        mostrar_mensaje("Presupuesto dado de baja correctamente.", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")


if __name__ == "__main__":
    menu_principal()