import re


# diccionario con los permisos por defecto de cada rol
roles_permisos = {
    "administrador": {"gastos", "categorias", "presupuestos", "reportes", "usuarios"},
    "editor": {"gastos", "categorias", "presupuestos"},
    "lector": {"reportes"}
}
# lista principal de usuarios guardados
# los permisos son sets para manejar quien entra a donde
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

# valida que la clave tenga al menos 6 caracteres una mayuscula y numeros
def validar_password(password):
    # primero me fijo el largo
    if len(password) < 6:
        return False
    
    # busco si tiene alguna mayuscula entre la A y la Z
    tiene_mayuscula = re.search("[A-Z]", password)
    
    # busco si tiene algun numero del 0 al 9
    tiene_numero = re.search("[0-9]", password)
    
    # si tiene ambas cosas devuelve True sino False
    if tiene_mayuscula and tiene_numero:
        return True
    else:
        return False

# muestra todos los users cargados
def listar_usuarios():
    print("\n--- lista de usuarios del sistema ---")
    for u in usuarios:
        print(f"ID: {u['id']} | User: {u['user']} | Rol: {u['rol']} | Permisos: {list(u['permisos'])}")

# crea usuario nuevo pidiendo datos y seteando permisos segun el rol
def registrar_usuario():
    print("\n--- nuevo usuario ---")
    nuevo_id = usuarios[-1]["id"] + 1 if len(usuarios) > 0 else 1
    
    username = input("ingrese nombre de usuario: ")
    # validamos que no este repetido
    if [u for u in usuarios if u["user"] == username]:
        print("ese usuario ya existe")
        return

    password = input("ingrese contraseña (min 6 letras 1 mayuscula y numeros): ")
    while not validar_password(password):
        print("clave invalida no cumple requisitos")
        password = input("ingrese otra contraseña valida: ")
    print("roles disponibles: 1. admin  2. editor  3. lector")
    opc = input("elija rol (1/2/3): ")
    
    if opc == "1":
        rol = "administrador"
        permisos = {"gastos", "categorias", "presupuestos", "reportes", "usuarios"}
    elif opc == "2":
        rol = "editor"
        permisos = {"gastos", "categorias", "presupuestos"}
    else:
        rol = "lector"
        permisos = {"reportes"}

    nuevo = {
        "id": nuevo_id,
        "user": username,
        "pass": password,
        "rol": rol,
        "permisos": permisos
    }
    usuarios.append(nuevo)
    print("usuario registrado con exito")

# funcion para chequear si el usuario puede entrar a una opcion usando sets
def verificar_permiso(usuario, permiso_requerido):
    # meto el permiso en un set chiquito y uso issubset
    permiso_a_revisar = {permiso_requerido}
    if permiso_a_revisar.issubset(usuario["permisos"]):
        return True
    return False

# funcion para modificar permisos a un usuario o a todo un rol
def modificar_permisos():
    print("\n--- MODIFICAR PERMISOS ---")
    print("1. modificar permisos a un usuario")
    print("2. modificar permisos a un rol completo")
    tipo = input("elija opcion: ")

    if tipo == "1":
        listar_usuarios()
        id_ingresado = input("\ningrese id del usuario: ")
        if not id_ingresado.isdigit():
            print("el id tiene que ser un numero")
            return
        id_buscar = int(id_ingresado)

        usuario_encontrado = None
        for u in usuarios:
            if u["id"] == id_buscar:
                usuario_encontrado = u
                break

        if not usuario_encontrado:
            print("no se encontro ese usuario")
            return

        print(f"permisos actuales de {usuario_encontrado['user']}: {usuario_encontrado['permisos']}")
        print("1. agregar permisos  2. quitar permisos")
        accion = input("elija que hacer: ")

        print("ingrese permisos separados por espacio (ej: gastos reportes):")
        entrada_permisos = input("permisos: ")
        # paso las palabras escritas a un set
        nuevos_permisos = set(entrada_permisos.split())

        if accion == "1":
            # uso union de sets para sumarle los permisos nuevos
            usuario_encontrado["permisos"] = usuario_encontrado["permisos"] | nuevos_permisos
            print("permisos agregados joya")
        elif accion == "2":
            # uso resta de sets para sacarle los permisos
            usuario_encontrado["permisos"] = usuario_encontrado["permisos"] - nuevos_permisos
            print("permisos quitados joya")
        else:
            print("opcion no valida")

    elif tipo == "2":
        print("\nroles disponibles: administrador, editor, lector")
        rol = input("ingrese el nombre del rol a cambiar: ").lower()

        if rol not in roles_permisos:
            print("ese rol no existe")
            return

        print(f"permisos actuales del rol {rol}: {roles_permisos[rol]}")
        print("1. agregar permisos  2. quitar permisos")
        accion = input("elija que hacer: ")

        print("ingrese permisos separados por espacio (ej: gastos reportes):")
        entrada_permisos = input("permisos: ")
        set_cambios = set(entrada_permisos.split())

        if accion == "1":
            # union al rol
            roles_permisos[rol] = roles_permisos[rol] | set_cambios
            print(f"permisos agregados al rol {rol}")
        elif accion == "2":
            # resta al rol
            roles_permisos[rol] = roles_permisos[rol] - set_cambios
            print(f"permisos quitados al rol {rol}")
        else:
            print("opcion no valida")
            return

        # preguntamos si quiere que los usuarios con ese rol se actualicen tambien
        actualizar = input("queres actualizar a todos los usuarios que tienen este rol? (s/n): ")
        if actualizar == "s":
            for u in usuarios:
                if u["rol"] == rol:
                    u["permisos"] = roles_permisos[rol].copy()
            print("usuarios actualizados con el nuevo rol")

    else:
        print("opcion no valida")
usuario_actual = usuarios[0]  # admin
print("--- test permiso individual ---")
print(f" {usuario_actual['user']} tiene gastos?:", verificar_permiso(usuario_actual, "gastos"))
print(f" {usuario_actual['user']} tiene usuarios?:", verificar_permiso(usuario_actual, "usuarios"))
print("\n--- probando modificar permisos ---")
modificar_permisos()
listar_usuarios()