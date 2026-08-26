from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()
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
Monto_limite = ["120.0", "45.0", "25.0", "58.0", "80.0"]
Id_CategoriaP = ["1", "2", "3", "4", "5"]
EstadoP = ["Activo", "Activo", "Activo", "Activo", "Activo"]
presupuestos = [Id_Presupuesto, Periodo_Presupuesto, Monto_limite, Id_CategoriaP, EstadoP]
encabezadosP = ["Id_Presupuesto", "Periodo", "Monto Limite", "Id_Categoria"]

# Gastos
NombreG = ["Supermercado", "Gasolina", "Cine", "Farmacia", "Curso online"]
Id_Gasto = ["1", "2", "3", "4", "5"]
FechaG = ["01/08/2026", "02/08/2026", "03/08/2026", "04/08/2026", "05/08/2026"]
MontoG = ["100.0", "40.0", "20.0", "50.0", "70.0"]
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
gastos = [Id_Gasto, NombreG, FechaG, MontoG, DescripcionG, Id_CatGasto, Id_PresGasto, EstadoG]
encabezadosG = ["Id_Gasto", "Nombre", "Fecha", "Monto", "Descripcion", "Id_Categoria", "Id_Presupuesto"]

## ===================
## FUNCIONES RICH
## ===================

## FUNCIONES RICH


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

    tabla_menu.add_row("0", "Salir")

    console.print()
    console.print(tabla_menu)
    console.print()

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

## FUNCIONES DE VALIDACION

def pedir_monto(mensaje):
    monto_valido = False
    resultado = 0.0
    while not monto_valido:
        entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] ").strip()
        if len(entrada) == 0:
            mostrar_mensaje("El campo no puede estar vacío.", "error")
        else:
            entrada_normalizada = entrada.replace(",", ".")
            partes = entrada_normalizada.split(".")
            es_num = False
            if len(partes) == 1 and partes[0].isdigit():
                es_num = True
            elif len(partes) == 2 and (partes[0].isdigit() or partes[0] == "") and partes[1].isdigit():
                if not (partes[0] == "" and len(partes[1]) == 0):
                    es_num = True
            if es_num:
                valor = float(entrada_normalizada)
                if valor > 0:
                    resultado = valor
                    monto_valido = True
                else:
                    mostrar_mensaje("El monto debe ser un número mayor a cero.", "alerta")
            else:
                mostrar_mensaje("Error: el formato introducido no es un número válido.", "error")
    return resultado


def pedir_monto_opcional(mensaje, valor_actual):
    monto_valido = False
    resultado = float(valor_actual)
    while not monto_valido:
        entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] [yellow][${valor_actual}][/yellow]: ").strip()
        if len(entrada) == 0:
            monto_valido = True
        else:
            entrada_normalizada = entrada.replace(",", ".")
            partes = entrada_normalizada.split(".")
            es_num = False
            if len(partes) == 1 and partes[0].isdigit():
                es_num = True
            elif len(partes) == 2 and (partes[0].isdigit() or partes[0] == "") and partes[1].isdigit():
                if not (partes[0] == "" and len(partes[1]) == 0):
                    es_num = True
            if es_num:
                valor = float(entrada_normalizada)
                if valor > 0:
                    resultado = valor
                    monto_valido = True
                else:
                    mostrar_mensaje("El monto debe ser un número mayor a cero.", "alerta")
            else:
                mostrar_mensaje("Error: el formato introducido no es un número válido.", "error")
    return resultado


def solicitar_y_verificar_fecha():
    fecha_valida = False
    resultado_fecha = ""
    while not fecha_valida:
        entrada = console.input("[bold cyan]Ingresa la fecha (DD/MM/AAAA):[/bold cyan] ").strip()
        partes = entrada.split("/")
        if len(partes) == 3 and partes[0].isdigit() and partes[1].isdigit() and partes[2].isdigit():
            dia = int(partes[0])
            mes = int(partes[1])
            anio = int(partes[2])
            es_bisiesto = anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)
            dias_por_mes = [31, 29 if es_bisiesto else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if 1 <= mes <= 12 and 1 <= dia <= dias_por_mes[mes - 1] and anio > 0:
                resultado_fecha = f"{dia:02d}/{mes:02d}/{anio:04d}"
                fecha_valida = True
            else:
                mostrar_mensaje("Fecha inválida en el calendario.", "error")
        else:
            mostrar_mensaje("Formato incorrecto. Use DD/MM/AAAA.", "error")
    return resultado_fecha


def pedir_texto_no_vacio(mensaje):
    texto_valido = False
    resultado = ""
    while not texto_valido:
        entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] ").strip()
        if len(entrada) > 0:
            resultado = entrada
            texto_valido = True
        else:
            mostrar_mensaje("Este campo no puede estar vacío.", "error")
    return resultado


def pedir_opcional(mensaje, valor_actual):
    entrada = console.input(f"[bold cyan]{mensaje}[/bold cyan] [yellow][{valor_actual}][/yellow]: ").strip()
    resultado = valor_actual
    if len(entrada) > 0:
        resultado = entrada
    return resultado


def pedir_id_existente(mensaje, lista_ids, lista_estados):
    id_valido = False
    resultado_id = ""
    while not id_valido:
        entrada = pedir_texto_no_vacio(mensaje)
        encontrado = False
        for i in range(len(lista_ids)):
            if lista_ids[i] == entrada and str(lista_estados[i]).upper() == "ACTIVO":
                encontrado = True
        if encontrado:
            resultado_id = entrada
            id_valido = True
        else:
            mostrar_mensaje("El ID ingresado no existe o no está activo.", "error")
    return resultado_id

def obtener_nombre_categoria(id_cat):
    for i in range(len(Id_Categoria)):
        if Id_Categoria[i] == str(id_cat):
            return NombreC[i]
    return "Sin Categoría"


def obtener_periodo_presupuesto(id_pres):
    for i in range(len(Id_Presupuesto)):
        if Id_Presupuesto[i] == str(id_pres):
            return Periodo_Presupuesto[i]
    return "Sin Presupuesto"

def seleccionar_categoria():
    console.print("\n[bold cyan]Seleccione una Categoría:[/bold cyan]")
    activas_idx = []
    for i in range(len(NombreC)):
        if str(EstadoC[i]).upper() == "ACTIVO":
            activas_idx.append(i)
            console.print(f"  [yellow]{len(activas_idx)}[/yellow]. {NombreC[i]} ({DescripcionC[i]})")
    
    valido = False
    id_seleccionado = ""
    while not valido:
        opc = pedir_texto_no_vacio("Ingrese el número de la categoría: ")
        if opc.isdigit():
            num = int(opc)
            if 1 <= num <= len(activas_idx):
                idx_real = activas_idx[num - 1]
                id_seleccionado = Id_Categoria[idx_real]
                valido = True
            else:
                mostrar_mensaje("Número fuera de rango.", "error")
        else:
            mostrar_mensaje("Debe ingresar un número.", "error")
    return id_seleccionado

def seleccionar_gasto():
    console.print("\n[bold cyan]Seleccione un Gasto:[/bold cyan]")
    activas_idx = []
    for i in range(len(NombreG)):
        if str(EstadoC[i]).upper() == "ACTIVO":
            activas_idx.append(i)
            console.print(f"  [yellow]{len(activas_idx)}[/yellow]. {NombreG[i]} ({DescripcionG[i]})")
    
    valido = False
    id_seleccionado = ""
    while not valido:
        opc = pedir_texto_no_vacio("Ingrese el número de la categoría: ")
        if opc.isdigit():
            num = int(opc)
            if 1 <= num <= len(activas_idx):
                idx_real = activas_idx[num - 1]
                id_seleccionado = Id_Gasto[idx_real]
                valido = True
            else:
                mostrar_mensaje("Número fuera de rango.", "error")
        else:
            mostrar_mensaje("Debe ingresar un número.", "error")
    return id_seleccionado


def seleccionar_presupuesto():
    console.print("\n[bold cyan]Seleccione un Presupuesto:[/bold cyan]")
    activas_idx = []
    for i in range(len(Periodo_Presupuesto)):
        if str(EstadoP[i]).upper() == "ACTIVO":
            activas_idx.append(i)
            cat_nom = obtener_nombre_categoria(Id_CategoriaP[i])
            console.print(f"  [yellow]{len(activas_idx)}[/yellow]. {cat_nom} | Período: {Periodo_Presupuesto[i]} (Límite: ${Monto_limite[i]})")
    
    valido = False
    id_seleccionado = ""
    while not valido:
        opc = pedir_texto_no_vacio("Ingrese el número del presupuesto: ")
        if opc.isdigit():
            num = int(opc)
            if 1 <= num <= len(activas_idx):
                idx_real = activas_idx[num - 1]
                id_seleccionado = Id_Presupuesto[idx_real]
                valido = True
            else:
                mostrar_mensaje("Número fuera de rango.", "error")
        else:
            mostrar_mensaje("Debe ingresar un número.", "error")
    return id_seleccionado

# ====================
## FUNCIONES MATRICES
# ====================
def obtener_matriz(lista):
    matriz = []
    total_filas = len(lista[0])
    total_columnas = len(lista)
    for col in range(total_filas):
        fila = []
        for fil in range(total_columnas):
            fila.append(lista[fil][col])
        matriz.append(fila)
    return matriz

# MOSTRAR MATRICES
def mostrar_matriz(matriz, encabezados, titulo_tabla):
    if not matriz:
        mostrar_mensaje("No hay datos cargados.", tipo="error")
        return

    filas_activas = [fila for fila in matriz if str(fila[-1]).upper() == "ACTIVO"]

    if not filas_activas:
        mostrar_mensaje("No hay registros activos para mostrar.", tipo="alerta")
        return

    cant_encabezados = len(encabezados)
    cant_columnas_datos = len(matriz[0]) - 1
    total_columnas = (
        cant_encabezados
        if cant_encabezados < cant_columnas_datos
        else cant_columnas_datos
    )

    tabla = Table(
        title=f"[bold cyan]{titulo_tabla}[/bold cyan]",
        header_style="bold magenta",
        border_style="bright_blue",
    )

    for i in range(total_columnas):
        tabla.add_column(encabezados[i], justify="left", style="white")

    for fila in filas_activas:
        valores = [str(fila[i]) for i in range(total_columnas)]
        tabla.add_row(*valores)

    console.print()
    console.print(tabla)
    console.print()
    console.input("[dim]Presione ENTER para continuar...[/dim]")


def mostrar_categorias():
    encabezados = ["Categoría", "Descripción"]
    filas = []
    for i in range(len(NombreC)):
        if str(EstadoC[i]).upper() == "ACTIVO":
            filas.append([NombreC[i], DescripcionC[i]])
    renderizar_tabla(encabezados, filas, "Listado de Categorías")
    console.input("[dim]Presione ENTER para continuar...[/dim]")


def mostrar_presupuestos():
    encabezados = ["Período", "Categoría Asignada", "Monto Límite"]
    filas = []
    for i in range(len(Periodo_Presupuesto)):
        if str(EstadoP[i]).upper() == "ACTIVO":
            nombre_cat = obtener_nombre_categoria(Id_CategoriaP[i])
            monto_fmt = f"${float(Monto_limite[i]):.2f}"
            filas.append([Periodo_Presupuesto[i], nombre_cat, monto_fmt])
    renderizar_tabla(encabezados, filas, "Listado de Presupuestos")
    console.input("[dim]Presione ENTER para continuar...[/dim]")


def mostrar_gastos():
    encabezados = ["Gasto", "Fecha", "Monto", "Descripción", "Categoría", "Período Asignado"]
    filas = []
    for i in range(len(NombreG)):
        if str(EstadoG[i]).upper() == "ACTIVO":
            nombre_cat = obtener_nombre_categoria(Id_CatGasto[i])
            periodo_pres = obtener_periodo_presupuesto(Id_PresGasto[i])
            monto_fmt = f"$USD {float(MontoG[i]):,.2f}"
            filas.append([
                NombreG[i],
                FechaG[i],
                monto_fmt,
                DescripcionG[i],
                nombre_cat,
                periodo_pres
            ])
    renderizar_tabla(encabezados, filas, "Control General de Gastos")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

# =================
# SISTEMA DE CRUDS
# =================
## CRUD CATEGORIAS

def agregar_categoria():
    console.print("\n[bold green]--- [C] AGREGAR NUEVA CATEGORÍA ---[/bold green]")
    nuevo_id = str(len(Id_Categoria) + 1)
    nombre = pedir_texto_no_vacio("Ingrese nombre de la categoría: ")
    descripcion = pedir_texto_no_vacio("Ingrese descripción: ")

    Id_Categoria.append(nuevo_id)
    NombreC.append(nombre)
    DescripcionC.append(descripcion)
    EstadoC.append("Activo")
    mostrar_mensaje(f"Categoría '{nombre}' agregada con ID: {nuevo_id}", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")


def consultar_categoria():
    console.print("\n[bold yellow]--- [R] CONSULTAR / BUSCAR CATEGORÍAS ---[/bold yellow]")
    if not Id_Categoria:
        mostrar_mensaje("No hay categorías registradas.", "error")
        return

    busqueda = pedir_texto_no_vacio("Ingrese término de búsqueda (ID o Nombre): ").lower()
    coincidencias = []

    for i in range(len(Id_Categoria)):
        if busqueda == Id_Categoria[i].lower() or busqueda in NombreC[i].lower():
            coincidencias.append(i)

    if not coincidencias:
        mostrar_mensaje("No se encontraron coincidencias.", "alerta")
    else:
        tabla = Table(title=f"Resultados para '{busqueda}'", header_style="bold magenta")
        for enc in encabezadosC:
            tabla.add_column(enc)
        tabla.add_column("Estado")

        for idx in coincidencias:
            tabla.add_row(Id_Categoria[idx], NombreC[idx], DescripcionC[idx], EstadoC[idx])
        console.print(tabla)
        console.input("[dim]Presione ENTER para continuar...[/dim]")


def modificar_categoria():
    console.print("\n[bold blue]--- [U] MODIFICAR CATEGORÍA ---[/bold blue]")
    id_cat = seleccionar_categoria()
    if id_cat == "0":
        return

    idx = -1
    for i in range(len(Id_Categoria)):
        if Id_Categoria[i] == id_cat:
            idx = i

    if idx == -1:
        mostrar_mensaje("ID no encontrado.", "error")
        return

    NombreC[idx] = pedir_opcional("Nuevo nombre", NombreC[idx])
    DescripcionC[idx] = pedir_opcional("Nueva descripción", DescripcionC[idx])

    cambiar_est = pedir_texto_no_vacio(f"¿Cambiar estado actual ({EstadoC[idx]})? (s/n): ").lower()
    if cambiar_est == "s":
        EstadoC[idx] = "Inactivo" if EstadoC[idx] == "Activo" else "Activo"
        mostrar_mensaje(f"Estado cambiado a: {EstadoC[idx]}", "info")

    mostrar_mensaje("Categoría actualizada exitosamente.", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")


def eliminar_categoria():
    console.print("\n[bold red]--- [D] BAJA LÓGICA DE CATEGORÍA ---[/bold red]")
    id_cat = seleccionar_categoria()
    if id_cat == "0":
        return

    idx = -1
    for i in range(len(Id_Categoria)):
        if Id_Categoria[i] == id_cat:
            idx = i

    if idx == -1:
        mostrar_mensaje("ID no encontrado.", "error")
        return

    if EstadoC[idx] == "Inactivo":
        reactivar = pedir_texto_no_vacio("Ya está inactiva. ¿Desea reactivarla? (s/n): ").lower()
        if reactivar == "s":
            EstadoC[idx] = "Activo"
            mostrar_mensaje("Categoría reactivada.", "exito")
        return

    confirmar = pedir_texto_no_vacio(f"¿Dar de baja la categoría '{NombreC[idx]}'? (s/n): ").lower()
    if confirmar == "s":
        EstadoC[idx] = "Inactivo"
        mostrar_mensaje("Categoría dada de baja correctamente.", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

## CRUD PRESUPUESTOS

def agregar_presupuesto():
    console.print("\n[bold green]--- [C] AGREGAR NUEVO PRESUPUESTO ---[/bold green]")
    nuevo_id = str(len(Id_Presupuesto) + 1)
    console.print("[dim]Definición de período:[/dim]")
    console.print("Fecha de Inicio:")
    f_inicio = solicitar_y_verificar_fecha()
    console.print("Fecha de Fin:")
    f_fin = solicitar_y_verificar_fecha()
    periodo = f"{f_inicio}-{f_fin}"

    monto = str(pedir_monto("Ingrese monto límite: "))
    id_cat = seleccionar_categoria()

    Id_Presupuesto.append(nuevo_id)
    Periodo_Presupuesto.append(periodo)
    Monto_limite.append(monto)
    Id_CategoriaP.append(id_cat)
    EstadoP.append("Activo")

    mostrar_mensaje(f"Presupuesto agregado con ID: {nuevo_id}", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")


def consultar_presupuesto():
    console.print("\n[bold yellow]--- [R] CONSULTAR / BUSCAR PRESUPUESTO ---[/bold yellow]")
    if not Id_Presupuesto:
        mostrar_mensaje("No hay presupuestos registrados.", "error")
        return

    busqueda = pedir_texto_no_vacio("Ingrese término de búsqueda (ID, Periodo o ID Categoría): ").lower()
    coincidencias = []

    for i in range(len(Id_Presupuesto)):
        if (busqueda == Id_Presupuesto[i].lower()
            or busqueda in Periodo_Presupuesto[i].lower()
            or busqueda == Id_CategoriaP[i].lower()):
            coincidencias.append(i)

    if not coincidencias:
        mostrar_mensaje("No se encontraron coincidencias.", "alerta")
    else:
        tabla = Table(title=f"Resultados para '{busqueda}'", header_style="bold magenta")
        for enc in encabezadosP:
            tabla.add_column(enc)
        tabla.add_column("Estado")

        for idx in coincidencias:
            tabla.add_row(
                Id_Presupuesto[idx],
                Periodo_Presupuesto[idx],
                Monto_limite[idx],
                Id_CategoriaP[idx],
                EstadoP[idx],
            )
        console.print(tabla)
        console.input("[dim]Presione ENTER para continuar...[/dim]")


def modificar_presupuesto():
    console.print("\n[bold blue]--- [U] MODIFICAR PRESUPUESTO ---[/bold blue]")
    id_p = seleccionar_presupuesto()
    if id_p == "0":
        return

    idx = -1
    for i in range(len(Id_Presupuesto)):
        if Id_Presupuesto[i] == id_p:
            idx = i

    if idx == -1:
        mostrar_mensaje("ID no encontrado.", "error")
        return

    Periodo_Presupuesto[idx] = pedir_opcional("Nuevo periodo (DD/MM/AAAA-DD/MM/AAAA)", Periodo_Presupuesto[idx])
    Monto_limite[idx] = str(pedir_monto_opcional("Nuevo monto límite", Monto_limite[idx]))
    Id_CategoriaP[idx] = pedir_opcional("Nuevo ID Categoría", Id_CategoriaP[idx])

    cambiar_est = pedir_texto_no_vacio(f"¿Cambiar estado actual ({EstadoP[idx]})? (s/n): ").lower()
    if cambiar_est == "s":
        EstadoP[idx] = "Inactivo" if EstadoP[idx] == "Activo" else "Activo"
        mostrar_mensaje(f"Estado cambiado a: {EstadoP[idx]}", "info")

    mostrar_mensaje("Presupuesto actualizado exitosamente.", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")


def eliminar_presupuesto():
    console.print("\n[bold red]--- [D] BAJA LÓGICA DE PRESUPUESTO ---[/bold red]")
    id_p = seleccionar_presupuesto()
    if id_p == "0":
        return

    idx = -1
    for i in range(len(Id_Presupuesto)):
        if Id_Presupuesto[i] == id_p:
            idx = i

    if idx == -1:
        mostrar_mensaje("ID no encontrado.", "error")
        return

    if EstadoP[idx] == "Inactivo":
        reactivar = pedir_texto_no_vacio("Ya está inactivo. ¿Desea reactivarlo? (s/n): ").lower()
        if reactivar == "s":
            EstadoP[idx] = "Activo"
            mostrar_mensaje("Presupuesto reactivado.", "exito")
        return

    confirmar = pedir_texto_no_vacio(f"¿Dar de baja el presupuesto ID '{Id_Presupuesto[idx]}'? (s/n): ").lower()
    if confirmar == "s":
        EstadoP[idx] = "Inactivo"
        mostrar_mensaje("Presupuesto dado de baja correctamente.", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

## CRUD GASTOS

def agregar_gasto():
    console.print("\n[bold green]--- [C] AGREGAR NUEVO GASTO ---[/bold green]")
    nuevo_id = str(len(Id_Gasto) + 1)
    nombre = pedir_texto_no_vacio("Ingrese nombre del gasto (ej: Supermercado): ")
    fecha = solicitar_y_verificar_fecha()
    monto = str(pedir_monto("Ingrese monto del gasto: "))
    descripcion = pedir_texto_no_vacio("Ingrese descripción del gasto: ")

    console.print("\n[dim]Categorías activas:[/dim]")
    id_cat = seleccionar_categoria()

    console.print("\n[dim]Presupuestos activos:[/dim]")
    id_pres = seleccionar_presupuesto()                                                    

    Id_Gasto.append(nuevo_id)
    NombreG.append(nombre)
    FechaG.append(fecha)
    MontoG.append(monto)
    DescripcionG.append(descripcion)
    Id_CatGasto.append(id_cat)
    Id_PresGasto.append(id_pres)
    EstadoG.append("Activo")

    mostrar_mensaje(f"Gasto '{nombre}' registrado con ID: {nuevo_id}", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")


def consultar_gasto():
    console.print("\n[bold yellow]--- [R] CONSULTAR / BUSCAR GASTOS ---[/bold yellow]")
    if not NombreG:
        mostrar_mensaje("No hay gastos registrados.", "error")
        return

    busqueda = pedir_texto_no_vacio("Ingrese término de búsqueda (nombre, categoría, descripción o fecha): ").lower()
    coincidencias = []

    for i in range(len(NombreG)):
        nombre_cat = obtener_nombre_categoria(Id_CatGasto[i]).lower()
        campos = [NombreG[i].lower(), FechaG[i].lower(), DescripcionG[i].lower(), nombre_cat]
        
        coincide = False
        for campo in campos:
            if busqueda in campo:
                coincide = True
        if coincide:
            coincidencias.append(i)

    if not coincidencias:
        mostrar_mensaje("No se encontraron gastos que coincidan.", "alerta")
    else:
        tabla = Table(title=f"Resultados para '{busqueda}'", header_style="bold magenta", border_style="bright_blue")
        encabezados = ["Gasto", "Fecha", "Monto", "Descripción", "Categoría", "Presupuesto", "Estado"]
        for enc in encabezados:
            tabla.add_column(enc)

        for idx in coincidencias:
            nombre_cat = obtener_nombre_categoria(Id_CatGasto[idx])
            periodo_pres = obtener_periodo_presupuesto(Id_PresGasto[idx])
            tabla.add_row(
                NombreG[idx],
                FechaG[idx],
                f"${float(MontoG[idx]):.2f}",
                DescripcionG[idx],
                nombre_cat,
                periodo_pres,
                EstadoG[idx]
            )
        console.print(tabla)
        console.input("[dim]Presione ENTER para continuar...[/dim]")

def modificar_gasto():
    console.print("\n[bold blue]--- [U] MODIFICAR GASTO ---[/bold blue]")
    id_g = seleccionar_gasto()
    if id_g == "0":
        return

    idx = -1
    for i in range(len(Id_Gasto)):
        if Id_Gasto[i] == id_g:
            idx = i

    if idx == -1:
        mostrar_mensaje("ID no encontrado.", "error")
        return

    NombreG[idx] = pedir_opcional("Nuevo nombre", NombreG[idx])
    FechaG[idx] = pedir_opcional("Nueva fecha (DD/MM/AAAA)", FechaG[idx])
    MontoG[idx] = str(pedir_monto_opcional("Nuevo monto", MontoG[idx]))
    DescripcionG[idx] = pedir_opcional("Nueva descripción", DescripcionG[idx])

    cambiar_cat = pedir_texto_no_vacio("¿Desea cambiar la categoría? (s/n): ").lower()
    if cambiar_cat == "s":
        Id_CatGasto[idx] = seleccionar_categoria()

    cambiar_pres = pedir_texto_no_vacio("¿Desea cambiar el presupuesto? (s/n): ").lower()
    if cambiar_pres == "s":
        Id_PresGasto[idx] = seleccionar_presupuesto()

    cambiar_est = pedir_texto_no_vacio(f"¿Cambiar estado actual ({EstadoG[idx]})? (s/n): ").lower()
    if cambiar_est == "s":
        EstadoG[idx] = "Inactivo" if EstadoG[idx] == "Activo" else "Activo"
        mostrar_mensaje(f"Estado cambiado a: {EstadoG[idx]}", "info")

    mostrar_mensaje("Gasto actualizado exitosamente.", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def eliminar_gasto():
    console.print("\n[bold red]--- [D] BAJA LÓGICA DE GASTO ---[/bold red]")
    id_g = seleccionar_gasto()
    if id_g == "0":
        return

    idx = -1
    for i in range(len(Id_Gasto)):
        if Id_Gasto[i] == id_g:
            idx = i

    if idx == -1:
        mostrar_mensaje("ID no encontrado.", "error")
        return

    if EstadoG[idx] == "Inactivo":
        reactivar = pedir_texto_no_vacio("Ya está inactivo. ¿Desea reactivarlo? (s/n): ").lower()
        if reactivar == "s":
            EstadoG[idx] = "Activo"
            mostrar_mensaje("Gasto reactivado.", "exito")
        return

    confirmar = pedir_texto_no_vacio(f"¿Dar de baja el gasto ID '{Id_Gasto[idx]}'? (s/n): ").lower()
    if confirmar == "s":
        EstadoG[idx] = "Inactivo"
        mostrar_mensaje("Gasto dado de baja correctamente.", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

# SISTEMA DE MENUS

def menu_categorias():
    activo = True
    opciones = [
        "Mostrar categorías",
        "Consultar / Buscar categoría",
        "Agregar categoría",
        "Modificar categoría",
        "Baja lógica de categoría",
    ]
    while activo:
        mostrar_menu("GESTIÓN DE CATEGORÍAS", opciones)
        opc = pedir_texto_no_vacio("Seleccione una opción: ")

        if opc == "1":
            mostrar_categorias()
        elif opc == "2":
            consultar_categoria()
        elif opc == "3":
            agregar_categoria()
        elif opc == "4":
            modificar_categoria()
        elif opc == "5":
            eliminar_categoria()
        elif opc == "0":
            activo = False
        else:
            mostrar_mensaje("Opción no válida.", "error")


def menu_presupuestos():
    activo = True
    opciones = [
        "Mostrar presupuestos",
        "Consultar / Buscar presupuesto",
        "Agregar presupuesto",
        "Modificar presupuesto",
        "Baja lógica de presupuesto",
    ]
    while activo:
        mostrar_menu("GESTIÓN DE PRESUPUESTOS", opciones)
        opc = pedir_texto_no_vacio("Seleccione una opción: ")

        if opc == "1":
            mostrar_presupuestos()
        elif opc == "2":
            consultar_presupuesto()
        elif opc == "3":
            agregar_presupuesto()
        elif opc == "4":
            modificar_presupuesto()
        elif opc == "5":
            eliminar_presupuesto()
        elif opc == "0":
            activo = False
        else:
            mostrar_mensaje("Opción no válida.", "error")


def menu_gastos():
    activo = True
    opciones = [
        "Mostrar gastos",
        "Consultar / Buscar gasto",
        "Agregar gasto",
        "Modificar gasto",
        "Baja lógica de gasto",
    ]
    while activo:
        mostrar_menu("GESTIÓN DE GASTOS", opciones)
        opc = pedir_texto_no_vacio("Seleccione una opción: ")

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
        elif opc == "0":
            activo = False
        else:
            mostrar_mensaje("Opción no válida.", "error")


def menu_principal():
    ejecutando = True
    opciones = [
        "Gestión de Gastos (CRUD)",
        "Gestión de Presupuestos (CRUD)",
        "Gestión de Categorías (CRUD)",
        "Ver Todas las Tablas",
    ]
    while ejecutando:
        mostrar_menu("SISTEMA DE GESTION FINANCIERA",opciones)
        opcion = pedir_texto_no_vacio("Seleccione una opción: ")

        if opcion == "1":
            menu_gastos()
        elif opcion == "2":
            menu_presupuestos()
        elif opcion == "3":
            menu_categorias()
        elif opcion == "4":
            mostrar_categorias()
            mostrar_presupuestos()
            mostrar_gastos()
        elif opcion == "0":
            mostrar_mensaje("¡Gracias por utilizar el sistema! Hasta luego.", "info")
            ejecutando = False
        else:
            mostrar_mensaje("Opción no válida. Intente nuevamente.", "error")


if __name__ == "__main__":
    menu_principal()