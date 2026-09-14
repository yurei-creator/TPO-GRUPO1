import re

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

registrar_usuario()
listar_usuarios()