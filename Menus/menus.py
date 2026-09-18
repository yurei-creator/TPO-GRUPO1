from Func.Func_Rich import console, mostrar_mensaje, mostrar_menu
from Func.Func_Matriz import mostrar_categorias, mostrar_presupuestos, mostrar_gastos
from Func.Func_val import pedir_opcion_menu
from Crud.Crud_Cat import (
    agregar_categoria,
    consultar_categoria,
    modificar_categoria,
    eliminar_categoria
)
from Crud.Crud_Pres import (
    agregar_presupuesto,
    consultar_presupuesto,
    modificar_presupuesto,
    eliminar_presupuesto
)
from Crud.Crud_Gast import (
    agregar_gasto,
    consultar_gasto,
    consultar_gastos_por_rango_fechas,
    modificar_gasto,
    eliminar_gasto
)
from Crud.Crud_Usuarios import (
    verificar_permiso,
    listar_usuarios,
    registrar_usuario,
    modificar_permisos,
    eliminar_usuario
)
from Func.Func_Estadisticas import (
    mostrar_resumen_estadistico_completo,
    mostrar_promedios,
    mostrar_conteos,
    mostrar_porcentajes_relativos,
    mostrar_maximos_y_minimos,
    comparativa_gastos_vs_presupuestos,
    ordenar_gastos_interactivo,
    simulacion_proyeccion_inflacion
)

def menu_categorias(categoria, gastos, presupuestos, encabezadosC, encabezadosG):
    activo = True
    opciones = [
        "Mostrar todas las categorías",
        "Consultar / Buscar categoría",
        "Agregar categoría",
        "Modificar categoría",
        "Baja / Reactivación lógica de categoría",
    ]
    while activo:
        mostrar_menu("GESTIÓN DE CATEGORÍAS", opciones)
        opc = pedir_opcion_menu("Seleccione una opción:", ["0", "1", "2", "3", "4", "5"])

        if opc == "1":
            mostrar_categorias(categoria, encabezadosC)
        elif opc == "2":
            consultar_categoria(categoria, gastos, presupuestos, encabezadosC, encabezadosG)
        elif opc == "3":
            agregar_categoria(categoria)
        elif opc == "4":
            modificar_categoria(categoria)
        elif opc == "5":
            eliminar_categoria(categoria)
        elif opc == "0":
            activo = False

def menu_presupuestos(presupuestos, categoria, gastos, encabezadosP):
    activo = True
    opciones = [
        "Mostrar todos los presupuestos",
        "Consultar / Buscar presupuesto",
        "Agregar presupuesto",
        "Modificar presupuesto",
        "Baja / Reactivación lógica de presupuesto",
    ]
    while activo:
        mostrar_menu("GESTIÓN DE PRESUPUESTOS", opciones)
        opc = pedir_opcion_menu("Seleccione una opción:", ["0", "1", "2", "3", "4", "5"])

        if opc == "1":
            mostrar_presupuestos(presupuestos, categoria, encabezadosP)
        elif opc == "2":
            consultar_presupuesto(presupuestos, categoria, gastos, encabezadosP)
        elif opc == "3":
            agregar_presupuesto(presupuestos, categoria)
        elif opc == "4":
            modificar_presupuesto(presupuestos, categoria)
        elif opc == "5":
            eliminar_presupuesto(presupuestos, categoria)
        elif opc == "0":
            activo = False

def menu_gastos(gastos, categoria, presupuestos, encabezadosG):
    activo = True
    opciones = [
        "Mostrar todos los gastos",
        "Consultar / Buscar gasto específico",
        "Registrar nuevo gasto",
        "Modificar gasto",
        "Baja / Reactivación lógica de gasto",
        "Consultar gastos por rango de fechas",
    ]
    while activo:
        mostrar_menu("GESTIÓN DE GASTOS", opciones)
        opc = pedir_opcion_menu("Seleccione una opción:", ["0", "1", "2", "3", "4", "5", "6"])

        if opc == "1":
            mostrar_gastos(gastos, categoria, encabezadosG)
        elif opc == "2":
            consultar_gasto(gastos, categoria, presupuestos, encabezadosG)
        elif opc == "3":
            agregar_gasto(gastos, categoria, presupuestos)
        elif opc == "4":
            modificar_gasto(gastos, categoria)
        elif opc == "5":
            eliminar_gasto(gastos, categoria)
        elif opc == "6":
            consultar_gastos_por_rango_fechas(gastos, categoria, encabezadosG)
        elif opc == "0":
            activo = False

def menu_estadisticas(gastos, categoria, presupuestos, encabezadosG):
    activo = True
    opciones = [
        "Resumen Estadístico General Consolidado",
        "Reporte de Promedios (General y por Categoría)",
        "Conteo de Registros Totales y por Categoría",
        "Porcentajes Relativos de Gasto por Categoría",
        "Identificación de Valores Máximos y Mínimos",
        "Comparativa Gasto Real vs. Presupuesto Previsto",
        "Ordenamiento dinámico de gastos",
        "Estimación de variación e inflación",
    ]
    while activo:
        mostrar_menu("REPORTES Y ESTADÍSTICAS DEL SISTEMA", opciones)
        opc = pedir_opcion_menu("Seleccione una opción:", ["0", "1", "2", "3", "4", "5", "6", "7", "8"])

        if opc == "1":
            mostrar_resumen_estadistico_completo(gastos, categoria, presupuestos)
        elif opc == "2":
            mostrar_promedios(gastos, categoria)
        elif opc == "3":
            mostrar_conteos(gastos, categoria)
        elif opc == "4":
            mostrar_porcentajes_relativos(gastos, categoria)
        elif opc == "5":
            mostrar_maximos_y_minimos(gastos, categoria)
        elif opc == "6":
            comparativa_gastos_vs_presupuestos(gastos, categoria, presupuestos)
        elif opc == "7":
            ordenar_gastos_interactivo(gastos, categoria)
        elif opc == "8":
            simulacion_proyeccion_inflacion(gastos)
        elif opc == "0":
            activo = False

def menu_usuarios(usuario_actual=None):
    activo = True
    opciones = [
        "Listar usuarios registrados",
        "Registrar nuevo usuario",
        "Modificar permisos de usuario o rol",
        "Baja / Reactivación lógica de usuario",
    ]
    while activo:
        mostrar_menu("ADMINISTRACIÓN DE USUARIOS Y PERMISOS", opciones)
        opc = pedir_opcion_menu("Seleccione una opción:", ["0", "1", "2", "3", "4"])

        if opc == "1":
            listar_usuarios()
        elif opc == "2":
            registrar_usuario()
        elif opc == "3":
            modificar_permisos()
        elif opc == "4":
            eliminar_usuario(usuario_actual)
        elif opc == "0":
            activo = False

def menu_principal(usuario, categoria, presupuestos, gastos, encabezadosC, encabezadosP, encabezadosG):
    ejecutando = True

    modulos = [
        ("gastos", "Gestión de Gastos (CRUD)"),
        ("presupuestos", "Gestión de Presupuestos (CRUD)"),
        ("categorias", "Gestión de Categorías (CRUD)"),
        ("reportes", "Reportes y Estadísticas Financieras"),
        ("usuarios", "Administración de Usuarios y Permisos"),
    ]

    while ejecutando:
        disponibles = []
        for i in range(len(modulos)):
            permiso, texto = modulos[i]
            if verificar_permiso(usuario, permiso):
                disponibles.append((permiso, texto))

        opciones_texto = [d[1] for d in disponibles]
        mostrar_menu("SISTEMA DE CONTROL DE GASTOS PERSONALES Y FAMILIARES", opciones_texto)

        opciones_validas = ["0"]
        for i in range(len(disponibles)):
            opciones_validas.append(str(i + 1))

        opcion = pedir_opcion_menu("Seleccione una opción:", opciones_validas)

        if opcion == "0":
            mostrar_mensaje("¡Gracias por utilizar el sistema! Sesión finalizada.", "info")
            ejecutando = False
        else:
            indice = int(opcion) - 1
            permiso_elegido = disponibles[indice][0]

            if permiso_elegido == "gastos":
                menu_gastos(gastos, categoria, presupuestos, encabezadosG)
            elif permiso_elegido == "presupuestos":
                menu_presupuestos(presupuestos, categoria, gastos, encabezadosP)
            elif permiso_elegido == "categorias":
                menu_categorias(categoria, gastos, presupuestos, encabezadosC, encabezadosG)
            elif permiso_elegido == "reportes":
                menu_estadisticas(gastos, categoria, presupuestos, encabezadosG)
            elif permiso_elegido == "usuarios":
                menu_usuarios(usuario)

