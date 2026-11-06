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
    
    while True:
        username = console.input("[bold cyan]Ingrese nombre de usuario (0 para cancelar):[/bold cyan] ").strip()
        if username == "0":
            return
        if not username:
            mostrar_mensaje("El nombre de usuario no puede estar vacío.", "error")
            continue
        if any(u["user"] == username for u in usuarios):
            mostrar_mensaje("El nombre de usuario ingresado ya existe.", "error")
            continue
        break 

    while True:
        password = console.input("[bold cyan]Ingrese contraseña (mínimo 6 caracteres, 1 mayúscula y números, o 0 para cancelar):[/bold cyan] ").strip()
        if password == "0":
            return
        if not validar_password(password):
            mostrar_mensaje("La contraseña no cumple con los requisitos mínimos de seguridad.", "alerta")
            continue
        break

    console.print("\n[dim]Roles disponibles: 1. Administrador | 2. Editor | 3. Lector[/dim]")
    while True:
        opc = console.input("[bold cyan]Seleccione el rol (1/2/3, o 0 para cancelar):[/bold cyan] ").strip()
        if opc == "0":
            return
        if opc not in ("1", "2", "3"):
            mostrar_mensaje("Debe seleccionar 1, 2 o 3.", "error")
            continue
        break
    
    if opc == "1":
        rol, permisos = "administrador", roles_permisos["administrador"].copy()
    elif opc == "2":
        rol, permisos = "editor", roles_permisos["editor"].copy()
    else:
        rol, permisos = "lector", roles_permisos["lector"].copy()

    nuevo = {
        "id": nuevo_id, "user": username, "pass": password,
        "rol": rol, "permisos": permisos, "estado": "Activo"
    }
    usuarios.append(nuevo)
    mostrar_mensaje(f"Usuario '{username}' registrado exitosamente con ID {nuevo_id}.", "exito")
    console.input("\n[dim]Presione ENTER para continuar...[/dim]")

def eliminar_usuario(usuario_actual=None):
    console.print("\n[bold red]--- BAJA / REACTIVACIÓN LÓGICA DE USUARIO ---[/bold red]")
    if not usuarios:
        mostrar_mensaje("No hay usuarios registrados.", "error")
        console.input("\n[dim]Presione ENTER para continuar...[/dim]")
        return

    listar_usuarios()
    
    while True:
        id_ingresado = console.input("[bold cyan]Ingrese el ID del usuario a modificar estado (0 para cancelar):[/bold cyan] ").strip()
        
        if id_ingresado == "0":
            return

        try:
            id_buscar = int(id_ingresado)
        except ValueError:
            mostrar_mensaje("El ID ingresado debe ser un valor numérico.", "error")
            continue

        user_sel = next((u for u in usuarios if u["id"] == id_buscar), None)

        if not user_sel:
            mostrar_mensaje("No se encontró ningún usuario con el ID especificado.", "error")
            continue
            
        if user_sel["user"] == "admin":
            mostrar_mensaje("No está permitido dar de baja al administrador principal del sistema.", "alerta")
            continue
            
        if usuario_actual and user_sel["user"] == usuario_actual.get("user"):
            mostrar_mensaje("No puedes darte de baja a ti mismo mientras tu sesión esté activa.", "alerta")
            continue

        estado_actual = user_sel.get("estado", "Activo")
        if estado_actual == "Inactivo":
            while True:
                reactivar = console.input(f"[bold cyan]El usuario '{user_sel['user']}' está INACTIVO. ¿Desea reactivarlo? (s/n):[/bold cyan] ").strip().lower()
                if reactivar == "s":
                    user_sel["estado"] = "Activo"
                    mostrar_mensaje(f"Usuario '{user_sel['user']}' reactivado exitosamente.", "exito")
                    break
                elif reactivar == "n":
                    mostrar_mensaje("Operación cancelada.", "info")
                    break
                else:
                    mostrar_mensaje("Opción inválida. Ingrese 's' para sí o 'n' para no.", "error")
        else:
            while True:
                confirmar = console.input(f"[bold cyan]¿Está seguro de dar de baja al usuario '{user_sel['user']}'? (s/n):[/bold cyan] ").strip().lower()
                if confirmar == "s":
                    user_sel["estado"] = "Inactivo"
                    mostrar_mensaje(f"Usuario '{user_sel['user']}' dado de baja correctamente (Inactivo).", "exito")
                    break
                elif confirmar == "n":
                    mostrar_mensaje("Operación cancelada.", "info")
                    break
                else:
                    mostrar_mensaje("Opción inválida. Ingrese 's' para sí o 'n' para no.", "error")
        
        break

    console.input("\n[dim]Presione ENTER para continuar...[/dim]")

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
    console.print("0. Cancelar")
    
    while True:
        tipo = console.input("[bold cyan]Seleccione una opción (1/2/0):[/bold cyan] ").strip()
        if tipo in ("0", "1", "2"):
            break
        mostrar_mensaje("Opción no válida seleccionada.", "error")

    if tipo == "0":
        return

    if tipo == "1":
        listar_usuarios()
        while True:
            id_ingresado = console.input("[bold cyan]Ingrese el ID del usuario a modificar (0 para cancelar):[/bold cyan] ").strip()
            if id_ingresado == "0":
                return
                
            try:
                id_buscar = int(id_ingresado)
            except ValueError:
                mostrar_mensaje("El ID ingresado debe ser un valor numérico.", "error")
                continue

            usuario_encontrado = next((u for u in usuarios if u["id"] == id_buscar), None)

            if not usuario_encontrado:
                mostrar_mensaje("No se encontró ningún usuario con el ID especificado.", "error")
                continue
            
            if "permisos" not in usuario_encontrado:
                usuario_encontrado["permisos"] = set()
                
            permisos_actuales = ", ".join(sorted(list(usuario_encontrado["permisos"]))) if usuario_encontrado["permisos"] else "Ninguno"
            console.print(f"\n[bold]Usuario:[/bold] [yellow]{usuario_encontrado['user']}[/yellow]")
            console.print(f"[bold]Permisos actuales:[/bold] [green]{permisos_actuales}[/green]\n")
            
            mostrar_permisos_disponibles()
            
            while True:
                accion = console.input("\n[dim]Acciones: 1. Agregar | 2. Quitar[/dim]\n[bold cyan]Seleccione (1/2):[/bold cyan] ").strip()
                if accion in ("1", "2"):
                    break
                mostrar_mensaje("Opción de acción no válida.", "error")
            
            while True:
                entrada_permisos = console.input("[bold cyan]Permisos (separados por espacio):[/bold cyan] ").strip().lower()
                if not entrada_permisos:
                    mostrar_mensaje("Debe ingresar al menos un permiso.", "error")
                    continue
                nuevos_permisos = set(entrada_permisos.split())
                break
                
            if accion == "1":
                usuario_encontrado["permisos"] |= nuevos_permisos
                mostrar_mensaje("Permisos agregados exitosamente.", "exito")
            else:
                usuario_encontrado["permisos"] -= nuevos_permisos
                mostrar_mensaje("Permisos revocados exitosamente.", "exito")
            
            break 

    elif tipo == "2":
        while True:
            rol = console.input("\n[dim]Roles: administrador | editor | lector[/dim]\n[bold cyan]Ingrese el rol (0 para cancelar):[/bold cyan] ").strip().lower()
            if rol == "0":
                return
                
            if rol not in roles_permisos:
                mostrar_mensaje("El rol ingresado no existe en el sistema.", "error")
                continue
                
            permisos_rol = ", ".join(sorted(list(roles_permisos[rol]))) if roles_permisos[rol] else "Ninguno"
            console.print(f"\n[bold]Rol:[/bold] [yellow]{rol}[/yellow]\n[bold]Permisos actuales:[/bold] [green]{permisos_rol}[/green]\n")
            
            mostrar_permisos_disponibles()
            
            while True:
                accion = console.input("\n[dim]Acciones: 1. Agregar | 2. Quitar[/dim]\n[bold cyan]Seleccione (1/2):[/bold cyan] ").strip()
                if accion in ("1", "2"):
                    break
                mostrar_mensaje("Opción de acción no válida.", "error")

            while True:
                entrada_permisos = console.input("[bold cyan]Permisos (separados por espacio):[/bold cyan] ").strip().lower()
                if not entrada_permisos:
                    mostrar_mensaje("Debe ingresar al menos un permiso.", "error")
                    continue
                set_cambios = set(entrada_permisos.split())
                break

            if accion == "1":
                roles_permisos[rol] |= set_cambios
                mostrar_mensaje(f"Permisos agregados al rol '{rol}'.", "exito")
            else:
                roles_permisos[rol] -= set_cambios
                mostrar_mensaje(f"Permisos revocados del rol '{rol}'.", "exito")

            while True:
                actualizar = console.input("\n[bold cyan]¿Sincronizar en usuarios existentes con este rol? (s/n):[/bold cyan] ").strip().lower()
                if actualizar == "s":
                    for u in usuarios:
                        if u["rol"] == rol:
                            if "permisos" not in u:
                                u["permisos"] = set()
                            u["permisos"] = roles_permisos[rol].copy()
                    mostrar_mensaje("Usuarios actualizados.", "info")
                    break
                elif actualizar == "n":
                    break
                else:
                    mostrar_mensaje("Opción inválida. Ingrese 's' para sí o 'n' para no.", "error")
            
            break 

    console.input("\n[dim]Presione ENTER para continuar...[/dim]")

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