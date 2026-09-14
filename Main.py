from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from Backup import *

console = Console()
# Categorías
id_categoria = ["1", "2", "3", "4", "5"]
nombre_c = ["Alimentos", "Transporte", "Ocio", "Salud", "Educación"]
descripcion_c = [
    "Categoria de alimentos",
    "Categoria de transporte",
    "Categoria de ocio",
    "Categoria de salud",
    "Categoria de educación",
]
estado_c = ["Activo", "Activo", "Activo", "Activo", "Activo"]
categoria = [id_categoria, nombre_c, descripcion_c, estado_c]
encabezados_c = ["Id_Categoria", "Nombre", "Descripcion"]

# Presupuestos
id_presupuesto = ["1", "2", "3", "4", "5"]
periodo_presupuesto = [
    "01/08/2026-10/08/2026",
    "02/08/2026-12/08/2026",
    "03/08/2026-13/08/2026",
    "04/08/2026-14/08/2026",
    "05/08/2026-15/08/2026",
]
monto_limite = ["120.0", "45.0", "25.0", "58.0", "80.0"]
id_categoria_p = ["1", "2", "3", "4", "5"]
estado_p = ["Activo", "Activo", "Activo", "Activo", "Activo"]
presupuestos = [id_presupuesto, periodo_presupuesto, monto_limite, id_categoria_p, estado_p]
encabezados_p = ["Id_Presupuesto", "Periodo", "Monto Limite", "Id_Categoria"]

# Gastos
nombre_g = ["Supermercado", "Gasolina", "Cine", "Farmacia", "Curso online"]
id_gasto = ["1", "2", "3", "4", "5"]
fecha_g = ["01/08/2026", "02/08/2026", "03/08/2026", "04/08/2026", "05/08/2026"]
monto_g = ["100.0", "40.0", "20.0", "50.0", "70.0"]
descripcion_g = [
    "Compra de alimentos",
    "Llenado de tanque",
    "Entrada de cine",
    "Compra de medicamentos",
    "Pago de curso online",
]
id_categoria_gasto = ["1", "2", "3", "4", "5"]
id_presupuesto_gasto = ["1", "2", "3", "4", "5"]
estado_g = ["Activo", "Activo", "Activo", "Activo", "Activo"]
gastos = [id_gasto, nombre_g, fecha_g, monto_g, descripcion_g, id_categoria_gasto, id_presupuesto_gasto, estado_g]
encabezados_g = ["Id_Gasto", "Nombre", "Fecha", "Monto", "Descripcion", "Id_Categoria", "Id_Presupuesto"]


if __name__ == "__main__":
    menu_principal()