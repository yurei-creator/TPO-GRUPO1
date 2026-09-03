'''Datos de login'''
nombre="san"
contrasena="1234"
clave_login=(nombre,contrasena)



'''Datos'''

# Categorías
Id_Categoria = ["1", "2", "3", "4", "5"]
NombreC = ["Alimentos", "Transporte", "Ocio", "Salud", "Educación"]
DescripcionC = [
    "Categoria de alimentos",
    "Categoria de transporte",
    "Categoria de ocio",
    "Categoria de salud",
    "Categoria de educación",
]
EstadoC = ["Activo", "Activo", "Activo", "Activo", "Activo"]
categoria = [Id_Categoria, NombreC, DescripcionC, EstadoC]
encabezadosC = ["Id_Categoria", "Nombre", "Descripcion"]

# Presupuestos
Id_Presupuesto = ["1", "2", "3", "4", "5"]
Periodo_Presupuesto = [
    "01/08/2026-10/08/2026",
    "02/08/2026-12/08/2026",
    "03/08/2026-13/08/2026",
    "04/08/2026-14/08/2026",
    "05/08/2026-15/08/2026",
]
Monto_limite = [120.0, 45.0, 25.0, 58.0, 80.0]
Id_CategoriaP = ["1", "2", "3", "4", "5"]
EstadoP = ["Activo", "Activo", "Activo", "Activo", "Activo"]
presupuestos = [Id_Presupuesto, Periodo_Presupuesto, Monto_limite, Id_CategoriaP, EstadoP]
encabezadosP = ["Id_Presupuesto", "Periodo", "Monto Limite", "Id_Categoria"]

# Gastos
NombreG = ["Supermercado", "Gasolina", "Cine", "Farmacia", "Curso online"]
Id_Gasto = ["1", "2", "3", "4", "5"]
FechaG = ["01/08/2026", "02/08/2026", "03/08/2026", "04/08/2026", "05/08/2026"]
MontoG = [100.0, 40.0, 20.0, 50.0, 70.0]
DescripcionG = [
    "Compra de alimentos",
    "Llenado de tanque",
    "Entrada de cine",
    "Compra de medicamentos",
    "Pago de curso online",
]
Id_CatGasto = ["1", "2", "3", "4", "5"]
Id_PresGasto = ["1", "2", "3", "4", "5"]
EstadoG = ["Activo", "Activo", "Activo", "Activo", "Activo"]
gastos = [ NombreG, FechaG, MontoG, DescripcionG, Periodo_Presupuesto]
encabezadosG = ["Id_Gasto", "Nombre", "Fecha", "Monto", "Descripcion", "Id_Categoria", "Id_Presupuesto"]

'''datos de porcentaje'''
datos_porcentaje=[NombreG,MontoG]