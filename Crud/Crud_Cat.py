# Importar SOLO los datos q vamos a usar desde Datos.Datos.
# Hacer buenas practicas de pasaje de datos.
# Revisar las funciones xq seguro hay que retocarlas
from Func.Func_Rich import *
from Func.Auxiliares import *

# Categoria = [[ID],[NOMBRE],[DESCRIPCION],[ESTADO]]
# Encabezados = [ENCABEZADOS]


def agregar_categoria(categoria):
    console.print("\n[bold green]--- [C] AGREGAR NUEVA CATEGORÍA ---[/bold green]")
    nuevo_id = str(len(categoria[0]) + 1)
    nombre = pedir_texto_no_vacio("Ingrese nombre de la categoría: ")
    descripcion = pedir_texto_no_vacio("Ingrese descripción: ")

    categoria[0].append(nuevo_id)
    categoria[1].append(nombre)
    categoria[2].append(descripcion)
    categoria[3].append("Activo")
    mostrar_mensaje(f"Categoría '{nombre}' agregada con ID: {nuevo_id}", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def consultar_categoria(categoria,encabezados):
    console.print("\n[bold yellow]--- [R] CONSULTAR / BUSCAR CATEGORÍAS ---[/bold yellow]")
    if not categoria[0]:
        mostrar_mensaje("No hay categorías registradas.", "error")
        return

    busqueda = pedir_texto_no_vacio("Ingrese término de búsqueda (ID o Nombre): ").lower()
    coincidencias = []

    for i in range(len(categoria[0])):
        if busqueda == categoria[0][i].lower() or busqueda in categoria[1][i].lower():
            coincidencias.append(i)

    if not coincidencias:
        mostrar_mensaje("No se encontraron coincidencias.", "alerta")
    else:
        tabla = Table(title=f"Resultados para '{busqueda}'", header_style="bold magenta")
        for enc in encabezados:
            tabla.add_column(enc)
        tabla.add_column("Estado")

        for idx in coincidencias:
            tabla.add_row(categoria[0][idx], categoria[1][idx], categoria[2][idx], categoria[3][idx])
        console.print(tabla)
        console.input("[dim]Presione ENTER para continuar...[/dim]")

def modificar_categoria(categoria):
    console.print("\n[bold blue]--- [U] MODIFICAR CATEGORÍA ---[/bold blue]")
    id_cat = seleccionar_categoria()
    if id_cat == "0":
        return

    idx = -1
    for i in range(len(categoria[0])):
        if categoria[0][i] == id_cat:
            idx = i

    if idx == -1:
        mostrar_mensaje("ID no encontrado.", "error")
        return

    categoria[1][idx] = pedir_opcional("Nuevo nombre", categoria[1][idx])
    categoria[2][idx] = pedir_opcional("Nueva descripción", categoria[2][idx])

    cambiar_est = pedir_texto_no_vacio(f"¿Cambiar estado actual ({categoria[3][idx]})? (s/n): ").lower()
    if cambiar_est == "s":
        print(categoria)
        categoria[3][idx] = not categoria[3]
        mostrar_mensaje(f"Estado cambiado a: {categoria[3][idx]}", "info")
        print(categoria)

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