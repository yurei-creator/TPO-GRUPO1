import json

ruta_encabezadoC = "Datos/encabezadosC.json"
ruta_encabezadoG = "Datos/encabezadosG.json"
ruta_encabezadoP = "Datos/encabezadosP.json"
ruta_categoria = "Datos/categoria.json"
ruta_presupuesto = "Datos/presupuesto.json"
ruta_gastos = "Datos/gastos.json"
ruta_rolespermisos = "Datos/roles_permisos.json"
ruta_datos_permisos_disponibles = "Datos/datos_permisos_disponibles.json"
ruta_usuarios = "Datos/datos_usuarios.json"


'''conversion de encabezadoC'''
try:
    encabC = open(ruta_encabezadoC, "r")
    encabezadosC = json.load(encabC)
except:
    print("no se puede abrir el archivo encabezadoC")
finally:
    try:
        encabC.close()
    except Exception as e:
        print(f"no se pudo cerrar el archivo sobre el encabezadoC correctamente: {e}")



'''conversion de encabezadoG'''
try:
    encabG = open(ruta_encabezadoG, "r")
    encabezadosG = json.load(encabG)
except:
    print("no se puede abrir el archivo encabezadoG")
finally:
    try:
        encabG.close()
    except Exception as e:
        print(f"no se pudo cerrar el archivo sobre el encabezadoG correctamente: {e}")



'''conversion de encabezadoP'''
try:
    encabP = open(ruta_encabezadoP, "r")
    encabezadoP = json.load(encabP)
except:
    print("no se puede abrir el archivo encabezadoP")
finally:
    try:
        encabP.close()
    except Exception as e:
        print(f"no se pudo cerrar el archivo sobre el encabezadoP correctamente: {e}")



'''conversion de categoria'''
try:
    categ = open(ruta_categoria, "r")
    categoria = json.load(categ)
except:
    print("no se puede abrir el archivo categoria")
finally:
    try:
        categ.close()
    except Exception as e:
        print(f"no se pudo cerrar el archivo categoria correctamente: {e}")



'''conversion de presupuesto'''
try:
    pres = open(ruta_presupuesto, "r")
    presupuesto = json.load(pres)
except:
    print("no se puede abrir el archivo presupuesto")
finally:
    try:
        pres.close()
    except Exception as e:
        print(f"no se pudo cerrar el archivo presupuesto correctamente: {e}")



'''conversion de gastos'''
try:
    gas = open(ruta_gastos, "r")
    gastos = json.load(gas)
except:
    print("no se puede abrir el archivo gastos")
finally:
    try:
        gas.close()
    except Exception as e:
        print(f"no se pudo cerrar el archivo gastos correctamente: {e}")



'''conversion de rolespermisos'''
try:
    rol = open(ruta_rolespermisos, "r")
    roles_permisos = json.load(rol)
except:
    print("no se puede abrir el archivo roles_permisos")
finally:
    try:
        rol.close()
    except Exception as e:
        print(f"no se pudo cerrar el archivo roles_permisos correctamente: {e}")



'''conversion de datos_permisos_disponibles'''
try:
    permiso = open(ruta_datos_permisos_disponibles, "r")
    permisos_disponibles = json.load(permiso)
except:
    print("no se puede abrir el archivo sobre datos_permisos_disponibles")
finally:
    try:
        permiso.close()
    except Exception as e:
        print(f"no se pudo cerrar el archivo sobre datos_permisos_disponibles correctamente: {e}")



'''conversion de datos de usuarios'''
try:
    usu = open(ruta_usuarios, "r")
    usuarios = json.load(usu)
except:
    print("no se puede abrir el archivo usuarios")
finally:
    try:
        usu.close()
    except Exception as e:
        print(f"no se pudo cerrar el archivo usuarios correctamente: {e}")




