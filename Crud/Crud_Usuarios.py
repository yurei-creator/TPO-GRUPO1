import re
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# lista fija de todos los permisos que maneja el sistema
PERMISOS_DISPONIBLES = ["gastos", "categorias", "presupuestos", "reportes", "usuarios"]

# diccionario con los permisos por defecto de cada rol
roles_permisos = {
    "administrador": {"gastos", "categorias", "presupuestos", "reportes", "usuarios"},
    "editor": {"gastos", "categorias", "presupuestos"},
    "lector": {"reportes"}
}

# lista principal de usuarios guardados
usuarios = [
    {
        "id": 1,
        "user": "admin",
        "pass": "Admin1234",
        "rol": "administrador",
        "permisos": {"gastos", "categorias", "presupuestos", "reportes", "usuarios"}
    },
    {
        "id": 2,
        "user": "mateo",
        "pass": "Mateo2026",
        "rol": "editor",
        "permisos": {"gastos", "categorias", "presupuestos"}
    },
    {
        "id": 3,
        "user": "invitado",
        "pass": "User1234",
        "rol": "lector",
        "permisos": {"reportes"}
    }
]

# funcion auxiliar para mostrar carteles con estilo panel de rich
def mostrar_mensaje(texto, tipo="info"):
    estilos = {
        "info": ("cyan", "INFORMACIÓN"),
        "exito": ("green", "ÉXITO"),
        "alerta": ("yellow", "ADVERTENCIA"),
        "error": ("red", "ERROR")
    }
    color, titulo = estilos.get(tipo, ("white", "MENSAJE"))
    panel = Panel(
        f"[{color}]{texto}[/{color}]",
        title=f"[bold {color}]{titulo}[/bold {color}]",
        border_style=color,
        expand=False
    )
    console.print(panel)

# valida que la clave tenga al menos 6 caracteres una mayuscula y numeros
def validar_password(password):
    if len(password) < 6:
        return False
    tiene_mayuscula = re.search("[A-Z]", password)
    tiene_numero = re.search("[0-9]", password)
    if tiene_mayuscula and tiene_numero:
        return True
    return False

# muestra todos los usuarios en una tabla rich
def listar_usuarios():
    tabla = Table(title="[bold cyan]Listado de Usuarios Registrados[/bold cyan]", header_style="bold magenta", border_style="bright_blue")
    tabla.add_column("ID", justify="center", style="bold yellow")
    tabla.add_column("Usuario", justify="left", style="white")
    tabla.add_column("Rol", justify="left", style="cyan")
    tabla.add_column("Permisos Asignados", justify="left", style="green")

    for u in usuarios:
        permisos_texto = ", ".join(sorted(list(u["permisos"])))
        tabla.add_row(str(u["id"]), u["user"], u["rol"], permisos_texto)

    console.print()
    console.print(tabla)
    console.print()

# crea usuario nuevo pidiendo datos y seteando permisos segun el rol
def registrar_usuario():
    console.print("\n[bold green]--- REGISTRO DE NUEVO USUARIO ---[/bold green]")
    nuevo_id = usuarios[-1]["id"] + 1 if len(usuarios) > 0 else 1
    
    username = console.input("[bold cyan]Ingrese nombre de usuario:[/bold cyan] ").strip()
    if [u for u in usuarios if u["user"] == username]:
        mostrar_mensaje("El nombre de usuario ingresado ya existe.", "error")
        return

    password = console.input("[bold cyan]Ingrese contraseña (mínimo 6 caracteres, 1 mayúscula y números):[/bold cyan] ").strip()
    while not validar_password(password):
        mostrar_mensaje("La contraseña no cumple con los requisitos mínimos de seguridad.", "alerta")
        password = console.input("[bold cyan]Ingrese una contraseña válida:[/bold cyan] ").strip()

    console.print("\n[dim]Roles disponibles: 1. Administrador | 2. Editor | 3. Lector[/dim]")
    opc = console.input("[bold cyan]Seleccione el rol (1/2/3):[/bold cyan] ").strip()
    
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
        "permisos": permisos
    }
    usuarios.append(nuevo)
    mostrar_mensaje(f"Usuario '{username}' registrado exitosamente con ID {nuevo_id}.", "exito")

# funcion para chequear si el usuario puede entrar a una opcion usando sets
def verificar_permiso(usuario, permiso_requerido):
    permiso_a_revisar = {permiso_requerido}
    if permiso_a_revisar.issubset(usuario["permisos"]):
        return True
    return False

# funcion para mostrar los permisos que existen en el sistema
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

# funcion para modificar permisos a un usuario o a todo un rol
def modificar_permisos():
    console.print("\n[bold blue]--- ADMINISTRACIÓN DE PERMISOS ---[/bold blue]")
    console.print("1. Modificar permisos de un usuario específico")
    console.print("2. Modificar permisos globales de un rol")
    tipo = console.input("[bold cyan]Seleccione una opción:[/bold cyan] ").strip()

    if tipo == "1":
        listar_usuarios()
        id_ingresado = console.input("[bold cyan]Ingrese el ID del usuario a modificar:[/bold cyan] ").strip()
        if not id_ingresado.isdigit():
            mostrar_mensaje("El ID ingresado debe ser un valor numérico.", "error")
            return
        id_buscar = int(id_ingresado)

        usuario_encontrado = None
        for u in usuarios:
            if u["id"] == id_buscar:
                usuario_encontrado = u
                break

        if not usuario_encontrado:
            mostrar_mensaje("No se encontró ningún usuario con el ID especificado.", "error")
            return

        permisos_actuales = ", ".join(sorted(list(usuario_encontrado["permisos"])))
        console.print(f"\n[bold]Usuario:[/bold] [yellow]{usuario_encontrado['user']}[/yellow]")
        console.print(f"[bold]Permisos actuales:[/bold] [green]{permisos_actuales}[/green]\n")
        
        # mostramos la tabla de permisos disponibles
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

    elif tipo == "2":
        console.print("\n[dim]Roles configurables: administrador | editor | lector[/dim]")
        rol = console.input("[bold cyan]Ingrese el nombre del rol a configurar:[/bold cyan] ").strip().lower()

        if rol not in roles_permisos:
            mostrar_mensaje("El rol ingresado no existe en el sistema.", "error")
            return

        permisos_rol = ", ".join(sorted(list(roles_permisos[rol])))
        console.print(f"\n[bold]Rol seleccionado:[/bold] [yellow]{rol}[/yellow]")
        console.print(f"[bold]Permisos actuales del rol:[/bold] [green]{permisos_rol}[/green]\n")
        
        # mostramos la tabla de permisos disponibles
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
            return

        actualizar = console.input("\n[bold cyan]¿Desea sincronizar estos permisos en los usuarios existentes con este rol? (s/n):[/bold cyan] ").strip().lower()
        if actualizar == "s":
            for u in usuarios:
                if u["rol"] == rol:
                    u["permisos"] = roles_permisos[rol].copy()
            mostrar_mensaje("Todos los usuarios con dicho rol fueron actualizados.", "info")

    else:
        mostrar_mensaje("Opción no válida seleccionada.", "error")

# funcion de login con 3 intentos devolviendo el diccionario del user o vacio si falla
def login():
    console.print("\n[bold cyan]====================================================[/bold cyan]")
    console.print("[bold cyan]       ACCESO AL SISTEMA DE GESTION DE GASTOS      [/bold cyan]")
    console.print("[bold cyan]====================================================[/bold cyan]")
    intentos = 0
    max_intentos = 3
    
    while intentos < max_intentos:
        user = console.input("[bold]Usuario:[/bold] ").strip()
        clave = console.input("[bold]Contraseña:[/bold] ").strip()
        
        for u in usuarios:
            if u["user"] == user and u["pass"] == clave:
                mostrar_mensaje(f"Bienvenido, {u['user']}. Sesión iniciada como {u['rol'].capitalize()}.", "exito")
                return u
        
        intentos = intentos + 1
        restantes = max_intentos - intentos
        if restantes > 0:
            mostrar_mensaje(f"Credenciales incorrectas. Intentos restantes: {restantes}.", "alerta")
    
    mostrar_mensaje("Acceso bloqueado por alcanzar el límite máximo de intentos fallidos.", "error")
    return {}

if __name__ == "__main__":
    login()