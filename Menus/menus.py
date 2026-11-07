from Func.Func_Rich import console, mostrar_mensaje, mostrar_menu
from Func.Func_Matriz import mostrar_categorias, mostrar_presupuestos, cargar_matriz
from Func.Func_val import pedir_opcion_menu

from Crud.Crud_Categorias.Crud_Cat import (
    eliminar_categoria,
    mostrar_categorias,
    alta_categoria,
    modificar_categoria,
    buscar_categoria
    )

from Crud.Crud_Presupuestos.Crud_Pres import (
    mostrar_presupuestos,
    eliminar_presupuesto,
    modificar_presupuesto,
    agregar_presupuesto,
    buscar_presupuesto
)

from Datos.Datos import (
    categoria_ruta,
    presupuesto_ruta
)

from Crud.Crud_Gast import (
    mostrar_gastos,
    agregar_gasto,
    consultar_gasto,
    consultar_gastos_por_rango_fechas,
    modificar_gasto,
    eliminar_gasto,
    leer_gastos,
    gastos_a_matriz
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

def menu_categorias():
    activo = True
    opciones = (
        "Mostrar todas las categorías",
        "Consultar / Buscar categoría",
        "Agregar categoría",
        "Modificar categoría",
        "Baja / Reactivación lógica de categoría",
    )
    while activo:
        mostrar_menu("GESTIÓN DE CATEGORÍAS", opciones)
        opc = pedir_opcion_menu("Seleccione una opción:", ("0", "1", "2", "3", "4", "5"))

        if opc == "1":
            mostrar_categorias()
        elif opc == "2":
            buscar_categoria()
        elif opc == "3":
            alta_categoria()
        elif opc == "4":
            modificar_categoria()
        elif opc == "5":
            eliminar_categoria()
        elif opc == "0":
            activo = False

def menu_presupuestos():
    activo = True
    opciones = (
        "Mostrar todos los presupuestos",
        "Consultar / Buscar presupuesto",
        "Agregar presupuesto",
        "Modificar presupuesto",
        "Baja / Reactivación lógica de presupuesto",
    )
    while activo:
        mostrar_menu("GESTIÓN DE PRESUPUESTOS", opciones)
        opc = pedir_opcion_menu("Seleccione una opción:", ("0", "1", "2", "3", "4", "5"))

        if opc == "1":
            mostrar_presupuestos()
        elif opc == "2":
            buscar_presupuesto()
        elif opc == "3":
            agregar_presupuesto()
        elif opc == "4":
            modificar_presupuesto()
        elif opc == "5":
            eliminar_presupuesto()
        elif opc == "0":
            activo = False

def menu_gastos():
    activo = True
    opciones = (
        "Mostrar todos los gastos",
        "Consultar / Buscar gasto específico",
        "Registrar nuevo gasto",
        "Modificar gasto",
        "Baja / Reactivación lógica de gasto",
        "Consultar gastos por rango de fechas",
    )
    while activo:
        mostrar_menu("GESTIÓN DE GASTOS", opciones)
        opc = pedir_opcion_menu("Seleccione una opción:", ("0", "1", "2", "3", "4", "5", "6"))

        if opc == "1":
            mostrar_gastos()
        elif opc == "2":
            consultar_gasto()
        elif opc == "3":
            agregar_gasto()
        elif opc == "4":
            modificar_gasto()
        elif opc == "5":
            eliminar_gasto()
        elif opc == "6":
            consultar_gastos_por_rango_fechas()
        elif opc == "0":
            activo = False

def menu_estadisticas():
    activo = True
    opciones = (
        "Resumen Estadístico General Consolidado",
        "Reporte de Promedios (General y por Categoría)",
        "Conteo de Registros Totales y por Categoría",
        "Porcentajes Relativos de Gasto por Categoría",
        "Identificación de Valores Máximos y Mínimos",
        "Comparativa Gasto Real vs. Presupuesto Previsto",
        "Ordenamiento dinámico de gastos",
        "Estimación de variación e inflación",
      )
    gastos_json = leer_gastos()
    if gastos_json is None:
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return
    gastos = gastos_a_matriz(gastos_json)
    presupuestos = cargar_matriz(presupuesto_ruta)
    categoria= cargar_matriz(categoria_ruta)
    while activo:
        mostrar_menu("REPORTES Y ESTADÍSTICAS DEL SISTEMA", opciones)
        opc = pedir_opcion_menu("Seleccione una opción:", ("0", "1", "2", "3", "4", "5", "6", "7", "8"))


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
    opciones = (
        "Listar usuarios registrados",
        "Registrar nuevo usuario",
        "Modificar permisos de usuario o rol",
        "Baja / Reactivación lógica de usuario",
    )
    while activo:
        mostrar_menu("ADMINISTRACIÓN DE USUARIOS Y PERMISOS", opciones)
        opc = pedir_opcion_menu("Seleccione una opción:", ("0", "1", "2", "3", "4"))

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

def menu_principal(usuario, presupuestos, gastos, encabezadosC, encabezadosP, encabezadosG):
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
                menu_gastos()
            elif permiso_elegido == "presupuestos":
                menu_presupuestos()
            elif permiso_elegido == "categorias":
                menu_categorias()
            elif permiso_elegido == "reportes":
                menu_estadisticas()
            elif permiso_elegido == "usuarios":
                menu_usuarios(usuario)

