import re
from Func.Func_Rich import console, mostrar_mensaje, Table
from Datos.Datos import usuarios, roles_permisos, PERMISOS_DISPONIBLES

def validar_password(password):
    if len(password) < 6:
        return False
    tiene_mayuscula = re.search(r"[A-Z]", password)
    tiene_numero = re.search(r"[0-9]", password)
    if tiene_mayuscula and tiene_numero:
        return True
    return False

def listar_usuarios():
    tabla = Table(title="[bold cyan]Listado de Usuarios Registrados[/bold cyan]", header_style="bold magenta", border_style="bright_blue")
    tabla.add_column("ID", justify="center", style="bold yellow")
    tabla.add_column("Usuario", justify="left", style="white")
    tabla.add_column("Rol", justify="left", style="cyan")
    tabla.add_column("Permisos Asignados", justify="left", style="green")
    tabla.add_column("Estado", justify="center")

    for u in usuarios:
        permisos_texto = ", ".join(sorted(list(u["permisos"])))
        est = u.get("estado", "Activo")
        color_est = "green" if est == "Activo" else "red"
        tabla.add_row(str(u["id"]), u["user"], u["rol"], permisos_texto, f"[{color_est}]{est}[/{color_est}]")

    console.print()
    console.print(tabla)
    console.print()

def registrar_usuario():
    console.print("\n[bold green]--- REGISTRO DE NUEVO USUARIO ---[/bold green]")
    nuevo_id = usuarios[-1]["id"] + 1 if len(usuarios) > 0 else 1
    
    try:
        username = console.input("[bold cyan]Ingrese nombre de usuario:[/bold cyan] ").strip()
        if not username:
            raise ValueError("El nombre de usuario no puede estar vacío.")
        if [u for u in usuarios if u["user"] == username]:
            raise ValueError("El nombre de usuario ingresado ya existe.")
    except ValueError as e:
        mostrar_mensaje(str(e), "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    while True:
        try:
            password = console.input("[bold cyan]Ingrese contraseña (mínimo 6 caracteres, 1 mayúscula y números):[/bold cyan] ").strip()
            if not validar_password(password):
                raise ValueError("La contraseña no cumple con los requisitos mínimos de seguridad.")
            break
        except ValueError as e:
            mostrar_mensaje(str(e), "alerta")

    console.print("\n[dim]Roles disponibles: 1. Administrador | 2. Editor | 3. Lector[/dim]")
    while True:
        try:
            opc = console.input("[bold cyan]Seleccione el rol (1/2/3):[/bold cyan] ").strip()
            if opc not in ("1", "2", "3"):
                raise ValueError("Debe seleccionar 1, 2 o 3.")
            break
        except ValueError as e:
            mostrar_mensaje(str(e), "error")
    
    if opc == "1":
        rol = "administrador"
        permisos = roles_permisos["administrador"].copy()
    elif opc == "2":
        rol = "editor"
        permisos = roles_permisos["editor"].copy()
    else:
        rol = "lector"
        permisos = roles_permisos["lector"].copy()

    nuevo = {
        "id": nuevo_id,
        "user": username,
        "pass": password,
        "rol": rol,
        "permisos": permisos,
        "estado": "Activo"
    }
    usuarios.append(nuevo)
    mostrar_mensaje(f"Usuario '{username}' registrado exitosamente con ID {nuevo_id}.", "exito")
    console.input("[dim]Presione ENTER para continuar...[/dim]")

def eliminar_usuario(usuario_actual=None):
    console.print("\n[bold red]--- BAJA / REACTIVACIÓN LÓGICA DE USUARIO ---[/bold red]")
    if not usuarios:
        mostrar_mensaje("No hay usuarios registrados.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    listar_usuarios()
    id_ingresado = console.input("[bold cyan]Ingrese el ID del usuario a modificar estado (0 para cancelar):[/bold cyan] ").strip()
    if id_ingresado == "0":
        return

    try:
        id_buscar = int(id_ingresado)
    except ValueError:
        mostrar_mensaje("El ID ingresado debe ser un valor numérico.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    user_sel = None
    for u in usuarios:
        if u["id"] == id_buscar:
            user_sel = u
            break

    if not user_sel:
        mostrar_mensaje("No se encontró ningún usuario con el ID especificado.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    if user_sel["user"] == "admin":
        mostrar_mensaje("No está permitido dar de baja al administrador principal del sistema.", "alerta")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    if usuario_actual and user_sel["user"] == usuario_actual.get("user"):
        mostrar_mensaje("No puedes darte de baja a ti mismo mientras tu sesión esté activa.", "alerta")
        console.input("[dim]Presione ENTER para continuar...[/dim]")
        return

    estado_actual = user_sel.get("estado", "Activo")
    if estado_actual == "Inactivo":
        reactivar = console.input(f"[bold cyan]El usuario '{user_sel['user']}' está INACTIVO. ¿Desea reactivarlo? (s/n):[/bold cyan] ").strip().lower()
        if reactivar == "s":
            user_sel["estado"] = "Activo"
            mostrar_mensaje(f"Usuario '{user_sel['user']}' reactivado exitosamente.", "exito")
        else:
            mostrar_mensaje("Operación cancelada.", "info")
    else:
        confirmar = console.input(f"[bold cyan]¿Está seguro de dar de baja al usuario '{user_sel['user']}'? (s/n):[/bold cyan] ").strip().lower()
        if confirmar == "s":
            user_sel["estado"] = "Inactivo"
            mostrar_mensaje(f"Usuario '{user_sel['user']}' dado de baja correctamente (Inactivo).", "exito")
        else:
            mostrar_mensaje("Operación cancelada.", "info")

    console.input("[dim]Presione ENTER para continuar...[/dim]")

def verificar_permiso(usuario, permiso_requerido):
    try:
        permiso_a_revisar = {permiso_requerido}
        return permiso_a_revisar.issubset(usuario["permisos"])
    except (KeyError, TypeError, AttributeError):
        return False

def mostrar_permisos_disponibles():
    tabla_permisos = Table(title="[bold yellow]Permisos Disponibles del Sistema[/bold yellow]", border_style="yellow")
    tabla_permisos.add_column("Módulo", justify="left", style="white")
    tabla_permisos.add_column("Descripción de Acceso", justify="left", style="dim")
    
    tabla_permisos.add_row("gastos", "Acceso completo a la gestión de gastos")
    tabla_permisos.add_row("categorias", "Acceso completo a la gestión de categorías")
    tabla_permisos.add_row("presupuestos", "Acceso completo a la gestión de presupuestos")
    tabla_permisos.add_row("reportes", "Acceso a reportes, tablas generales y estadísticas")
    tabla_permisos.add_row("usuarios", "Administración de cuentas y permisos de acceso")
    
    console.print(tabla_permisos)

def modificar_permisos():
    console.print("\n[bold blue]--- ADMINISTRACIÓN DE PERMISOS ---[/bold blue]")
    console.print("1. Modificar permisos de un usuario específico")
    console.print("2. Modificar permisos globales de un rol")
    tipo = console.input("[bold cyan]Seleccione una opción (1/2):[/bold cyan] ").strip()

    if tipo == "1":
        listar_usuarios()
        id_ingresado = console.input("[bold cyan]Ingrese el ID del usuario a modificar:[/bold cyan] ").strip()
        try:
            id_buscar = int(id_ingresado)
        except ValueError:
            mostrar_mensaje("El ID ingresado debe ser un valor numérico.", "error")
            console.input("[dim]Presione ENTER para continuar...[/dim]")
            return

        usuario_encontrado = None
        for u in usuarios:
            if u["id"] == id_buscar:
                usuario_encontrado = u
                break

        if not usuario_encontrado:
            mostrar_mensaje("No se encontró ningún usuario con el ID especificado.", "error")
            console.input("[dim]Presione ENTER para continuar...[/dim]")
            return

        permisos_actuales = ", ".join(sorted(list(usuario_encontrado["permisos"])))
        console.print(f"\n[bold]Usuario:[/bold] [yellow]{usuario_encontrado['user']}[/yellow]")
        console.print(f"[bold]Permisos actuales:[/bold] [green]{permisos_actuales}[/green]\n")
        
        mostrar_permisos_disponibles()

        console.print("\n[dim]Acciones: 1. Agregar permisos | 2. Quitar permisos[/dim]")
        accion = console.input("[bold cyan]Seleccione acción (1/2):[/bold cyan] ").strip()

        entrada_permisos = console.input("[bold cyan]Ingrese los permisos separados por espacio:[/bold cyan] ").strip().lower()
        nuevos_permisos = set(entrada_permisos.split())

        if accion == "1":
            usuario_encontrado["permisos"] = usuario_encontrado["permisos"] | nuevos_permisos
            mostrar_mensaje("Permisos agregados exitosamente al usuario.", "exito")
        elif accion == "2":
            usuario_encontrado["permisos"] = usuario_encontrado["permisos"] - nuevos_permisos
            mostrar_mensaje("Permisos revocados exitosamente del usuario.", "exito")
        else:
            mostrar_mensaje("Opción de acción no válida.", "error")

        console.input("[dim]Presione ENTER para continuar...[/dim]")

    elif tipo == "2":
        console.print("\n[dim]Roles configurables: administrador | editor | lector[/dim]")
        rol = console.input("[bold cyan]Ingrese el nombre del rol a configurar:[/bold cyan] ").strip().lower()

        try:
            permisos_rol = ", ".join(sorted(list(roles_permisos[rol])))
        except KeyError:
            mostrar_mensaje("El rol ingresado no existe en el sistema.", "error")
            console.input("[dim]Presione ENTER para continuar...[/dim]")
            return

        console.print(f"\n[bold]Rol seleccionado:[/bold] [yellow]{rol}[/yellow]")
        console.print(f"[bold]Permisos actuales del rol:[/bold] [green]{permisos_rol}[/green]\n")
        
        mostrar_permisos_disponibles()

        console.print("\n[dim]Acciones: 1. Agregar permisos | 2. Quitar permisos[/dim]")
        accion = console.input("[bold cyan]Seleccione acción (1/2):[/bold cyan] ").strip()

        entrada_permisos = console.input("[bold cyan]Ingrese los permisos separados por espacio:[/bold cyan] ").strip().lower()
        set_cambios = set(entrada_permisos.split())

        if accion == "1":
            roles_permisos[rol] = roles_permisos[rol] | set_cambios
            mostrar_mensaje(f"Permisos agregados correctamente al rol '{rol}'.", "exito")
        elif accion == "2":
            roles_permisos[rol] = roles_permisos[rol] - set_cambios
            mostrar_mensaje(f"Permisos revocados correctamente del rol '{rol}'.", "exito")
        else:
            mostrar_mensaje("Opción no válida.", "error")
            console.input("[dim]Presione ENTER para continuar...[/dim]")
            return

        actualizar = console.input("\n[bold cyan]¿Desea sincronizar estos permisos en los usuarios existentes con este rol? (s/n):[/bold cyan] ").strip().lower()
        if actualizar == "s":
            for u in usuarios:
                if u["rol"] == rol:
                    u["permisos"] = roles_permisos[rol].copy()
            mostrar_mensaje("Todos los usuarios con dicho rol fueron actualizados.", "info")

        console.input("[dim]Presione ENTER para continuar...[/dim]")

    else:
        mostrar_mensaje("Opción no válida seleccionada.", "error")
        console.input("[dim]Presione ENTER para continuar...[/dim]")

def login():
    console.print("\n[bold cyan]====================================================[/bold cyan]")
    console.print("[bold cyan]       ACCESO AL SISTEMA DE GESTION DE GASTOS      [/bold cyan]")
    console.print("[bold cyan]====================================================[/bold cyan]")
    intentos = 0
    max_intentos = 3
    
    while intentos < max_intentos:
        user = "admin" #console.input("[bold]Usuario:[/bold] ").strip()
        clave = "Admin1234" #console.input("[bold]Contraseña:[/bold] ").strip()
        
        for u in usuarios:
            if u["user"] == user and u["pass"] == clave:
                if u.get("estado", "Activo") == "Inactivo":
                    mostrar_mensaje("El usuario se encuentra inactivo. Contacte al administrador.", "error")
                    return None
                mostrar_mensaje(f"Bienvenido, {u['user']}. Sesión iniciada como {u['rol'].capitalize()}.", "exito")
                return u
        
        intentos += 1
        restantes = max_intentos - intentos
        if restantes > 0:
            mostrar_mensaje(f"Credenciales incorrectas. Intentos restantes: {restantes}.", "alerta")
    
    mostrar_mensaje("Acceso bloqueado por alcanzar el límite máximo de intentos fallidos.", "error")
    return None