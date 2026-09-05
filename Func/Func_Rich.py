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
        tabla.add_row(*fila)

    console.print()
    console.print(tabla)
    console.print()