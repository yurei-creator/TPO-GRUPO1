# Datos iniciales del Sistema de Control de Gastos Personales y Familiares
# Modelado canónico en matrices bidimensionales (listas de listas por fila)

# Encabezados de entidades
encabezadosC = ["ID", "Nombre", "Descripcion", "Estado"]
encabezadosP = ["ID", "ID_Categoria", "Periodo", "Monto Limite", "Estado"]
encabezadosG = ["ID", "Fecha", "Monto", "ID_Categoria", "Descripcion", "Estado"]

# -------------------------------------------------------------------------
# Entidad: Categorías
# Fila: [ID, Nombre, Descripción, Estado]
# -------------------------------------------------------------------------
categoria = [
    ["1", "Alimentos", "Gastos de supermercado, carnicería y verdulería", "Activo"],
    ["2", "Transporte", "Combustible, pasajes y mantenimiento vehicular", "Activo"],
    ["3", "Ocio", "Salidas, cine, restaurantes y recreación", "Activo"],
    ["4", "Salud", "Farmacia, consultas médicas y medicamentos", "Activo"],
    ["5", "Educación", "Cursos, libros y materiales de estudio", "Activo"],
]

# -------------------------------------------------------------------------
# Entidad: Presupuestos
# Fila: [ID, ID_Categoria, Período, Monto Límite, Estado]
# -------------------------------------------------------------------------
presupuesto_ruta = "Datos/presupuestos.txt"
# -------------------------------------------------------------------------
# Entidad: Gastos (Entidad de Unión)
# Fila: [ID, Fecha, Monto, ID_Categoria, Descripción, Estado]
# -------------------------------------------------------------------------
gastos = [
    ["1", "01/08/2026", 12500.0, "1", "Supermercado compra semanal", "Activo"],
    ["2", "02/08/2026", 4500.0, "2", "Carga de combustible", "Activo"],
    ["3", "03/08/2026", 3200.0, "3", "Entradas de cine y combo", "Activo"],
    ["4", "04/08/2026", 1800.0, "4", "Farmacia medicamentos", "Activo"],
    ["5", "05/08/2026", 7500.0, "5", "Pago cuota curso online", "Activo"],
    ["6", "10/08/2026", 18200.0, "1", "Compra mensual supermercado", "Activo"],
    ["7", "12/08/2026", 6000.0, "2", "Recarga de tarjeta transporte", "Activo"],
    ["8", "15/08/2026", 5400.0, "3", "Cena con amigos", "Activo"],
]

# -------------------------------------------------------------------------
# Usuarios, Roles y Permisos (utiliza conjuntos 'set')
# -------------------------------------------------------------------------
PERMISOS_DISPONIBLES = ["gastos", "categorias", "presupuestos", "reportes", "usuarios"]

roles_permisos = {
    "administrador": {"gastos", "categorias", "presupuestos", "reportes", "usuarios"},
    "editor": {"gastos", "categorias", "presupuestos", "reportes"},
    "lector": {"reportes"}
}

usuarios = [
    {
        "id": 1,
        "user": "admin",
        "pass": "Admin1234",
        "rol": "administrador",
        "permisos": {"gastos", "categorias", "presupuestos", "reportes", "usuarios"},
        "estado": "Activo"
    },
    {
        "id": 2,
        "user": "familiar",
        "pass": "Familiar2026",
        "rol": "editor",
        "permisos": {"gastos", "categorias", "presupuestos", "reportes"},
        "estado": "Activo"
    },
    {
        "id": 3,
        "user": "invitado",
        "pass": "User1234",
        "rol": "lector",
        "permisos": {"reportes"},
        "estado": "Activo"
    }
]


import os

def cargar_presupuestos(ruta):
    presupuestos = []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                id_p, id_cat, periodo, monto, estado = linea.split("|")
                presupuestos.append([id_p, id_cat, periodo, float(monto), estado])
    except FileNotFoundError:
        pass  # primera ejecución: lista vacía
    return presupuestos



def guardar_presupuestos(presupuestos, ruta):
    with open(ruta, "w", encoding="utf-8") as archivo:
        for fila in presupuestos:
            archivo.write("|".join(str(campo) for campo in fila) + "\n")


def guardar_presupuestos(presupuestos, ruta=presupuesto_ruta):
    with open(ruta, "w", encoding="utf-8") as archivo:
        for fila in presupuestos:
            archivo.write("|".join(str(campo) for campo in fila) + "\n")