from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def mostrar_mensaje(texto, tipo="info"):
    estilos = {
        "info": ("cyan", "INFORMACIÓN"),
        "exito": ("green", "ÉXITO"),
        "alerta": ("yellow", "ADVERTENCIA"),
        "error": ("red", "ERROR"),
    }
    color, titulo = estilos.get(tipo, ("white", "MENSAJE"))
    panel = Panel(
        f"[{color}]{texto}[/{color}]",
        title=f"[bold {color}]{titulo}[/bold {color}]",
        border_style=color,
        expand=False,
    )
    console.print(panel)

def renderizar_tabla(encabezados, filas, titulo):
    if not filas:
        console.print(f"[yellow]No hay registros activos para {titulo.lower()}.[/yellow]")
        return

    tabla = Table(
        title=f"[bold cyan]{titulo}[/bold cyan]",
        header_style="bold magenta",
        border_style="bright_blue",
    )

    for enc in encabezados:
        tabla.add_column(enc, justify="left", style="white")

    for fila in filas:
        tabla.add_row(*[str(x) for x in fila])

    console.print()
    console.print(tabla)
    console.print()

def mostrar_menu(titulo, opciones):
    tabla_menu = Table(
        title=f"[bold cyan]{titulo}[/bold cyan]",
        show_header=True,
        header_style="bold magenta",
        border_style="bright_blue",
    )
    tabla_menu.add_column("Opción", justify="center", style="bold yellow")
    tabla_menu.add_column("Descripción", justify="left", style="white")

    for i in range(len(opciones)):
        numero_opcion = str(i + 1)
        nombre_opcion = opciones[i]
        tabla_menu.add_row(numero_opcion, nombre_opcion)

    tabla_menu.add_row("0", "Volver al menú anterior / Salir")

    console.print()
    console.print(tabla_menu)
    console.print()