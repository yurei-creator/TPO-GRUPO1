# Datos iniciales del Sistema de Control de Gastos Personales y Familiares
# Modelado canónico en matrices bidimensionales (listas de listas por fila)


# -------------------------------------------------------------------------
# Entidad: Categorías
# Fila: [ID, Nombre, Descripción, Estado]
# -------------------------------------------------------------------------
encabezadosG = ("ID", "Fecha", "Monto", "ID_Categoria", "Descripcion", "Estado")
encabezadosP = ("ID", "ID_Categoria", "Periodo", "Monto Limite", "Estado")
encabezadosC = ("ID", "Nombre", "Descripcion", "Estado")
categoria_ruta = r"Datos/categorias.txt"
presupuesto_ruta = r"Datos/presupuestos.txt"
ruta_gastos = r"Datos/gastos.json"
# -------------------------------------------------------------------------
# Entidad: Presupuestos
# Fila: [ID, ID_Categoria, Período, Monto Límite, Estado]
# -------------------------------------------------------------------------
presupuestos = [
    ["1", "1", "01/08/2026-31/08/2026", 50000.0, "Activo"],
    ["2", "2", "01/08/2026-31/08/2026", 20000.0, "Activo"],
    ["3", "3", "01/08/2026-31/08/2026", 15000.0, "Activo"],
    ["4", "4", "01/08/2026-31/08/2026", 10000.0, "Activo"],
    ["5", "5", "01/08/2026-31/08/2026", 12000.0, "Activo"],
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