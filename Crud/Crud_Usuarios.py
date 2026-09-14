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

listar_usuarios()
Valida = validar_password("1234") # da false porque no tiene mayuscula y es menor a 6 caracteres
print(Valida)
Valida = validar_password("123456") # da false porque no tiene mayuscula
print(Valida)
Valida = validar_password("123456A") # da true porque tiene mayuscula y es mayor a 6 caracteres
print(Valida)
Valida = validar_password("hola_mundo") # da false porque no tiene mayuscula ni numeros
print(Valida)
Valida = validar_password("Hola_mundo") # da false porque no tiene numeros
print(Valida)
Valida = validar_password("Hola_mundo1") # da true porque tiene mayuscula y numeros
print(Valida)
Valida = validar_password(usuarios[0]["pass"]) # da true porque cumple con los criterios
print(Valida)