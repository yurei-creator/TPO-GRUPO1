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
encabezadosG = ["Id_Gasto", "Nombre", "Fecha", "Monto", "Descripcion", "Estado"]

gastos = [
    {
        "id_gasto": "1",
        "nombre": "Supermercado",
        "fecha": "01/08/2026",
        "monto": 100.0,
        "descripcion": "Compra de alimentos",
        "estado": True
    },
    {
        "id_gasto": "2",
        "nombre": "Gasolina",
        "fecha": "02/08/2026",
        "monto": 40.0,
        "descripcion": "Llenado de tanque",
        "estado": True
    },
    {
        "id_gasto": "3",
        "nombre": "Cine",
        "fecha": "03/08/2026",
        "monto": 20.0,
        "descripcion": "Entrada de cine",
        "estado": True
    },
    {
        "id_gasto": "4",
        "nombre": "Farmacia",
        "fecha": "04/08/2026",
        "monto": 50.0,
        "descripcion": "Compra de medicamentos",
        "estado": True
    },
    {
        "id_gasto": "5",
        "nombre": "Curso online",
        "fecha": "05/08/2026",
        "monto": 70.0,
        "descripcion": "Pago de curso online",
        "estado": True
    }
]

'''datos de porcentaje'''
datos_porcentaje = [
    [g["nombre"] for g in gastos], 
    [g["monto"] for g in gastos]
]