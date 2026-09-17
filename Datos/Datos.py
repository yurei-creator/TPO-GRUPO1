'''Datos de login'''
nombre="san"
contrasena="1234"
clave_login=(nombre,contrasena)



'''Datos
# Categorías
#testing
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
encabezadosC = ["Id_Categoria", "Nombre", "Descripcion", "Estado"]
'''
Id_Categoria = ["1", "2", "3"]
NombreC = ["Alimentos", "Transporte", "Ocio"]
DescripcionC = [
    "Categoria de alimentos",
    "Categoria de transporte",
    "Categoria de ocio"]
EstadoC = ["Activo", "Activo", "Activo"]
categoria = [Id_Categoria, NombreC, DescripcionC, EstadoC]
encabezadosC = ["ID", "Nombre", "Descripcion", "Estado"]

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

Cat_fk = ["2", "3", "1", "2", "1"]
EstadoP = ["Activo", "Activo", "Activo", "Activo", "Activo"]
presupuestos = [Id_Presupuesto, Cat_fk, Monto_limite, Periodo_Presupuesto, EstadoP]
encabezadosP = ["Id_Presupuesto", "ID-Cat-Nombre", "Periodo", "Monto Limite", "Estado"]

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
# ??? pq  creamos 90 listas de IDS si se suponen los ID vienen de las otras tablas
Id_CatGasto = ["1", "2", "3", "4", "5"]
Id_PresGasto = ["1", "2", "3", "4", "5"]
EstadoG = [True, True, True, True, True]
gastos = [ NombreG, FechaG, MontoG, DescripcionG, Periodo_Presupuesto, EstadoG]
encabezadosG = ["Id_Gasto", "Nombre", "Fecha", "Monto", "Descripcion", "Id_Categoria", "Id_Presupuesto"]

'''datos de porcentaje'''
datos_porcentaje=[NombreG,MontoG]