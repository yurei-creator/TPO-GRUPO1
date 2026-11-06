import json

ruta_encabezado = "Datos/encabezados.json"
ruta_categoria = "Datos/categorias.json"
ruta_permisos = "Datos/permisos.json"
ruta_usuarios = "Datos/datos_usuarios.json"


'''conversion de encabezados'''
try:
    encab = open(ruta_encabezado, "r", encoding="utf-8")
    datos_encabezados = json.load(encab)
    encabezadosC = datos_encabezados[0]
    encabezadosG = datos_encabezados[1]
    encabezadosP = datos_encabezados[2]
except:
    print("no se puede abrir un archivo ")
finally:
    try:
        encab.close()
    except Exception as e:
        print(f"no se pudo cerrar el archivo correctamente: {e}")



'''conversion de categorias'''
try:
    categ = open(ruta_categoria, "r", encoding="utf-8")
    dato_categoria = json.load(categ)
    categoria = dato_categoria[0]
    gastos = dato_categoria[1]
    presupuesto = dato_categoria[2]
except:
    print("no se puede abrir el archivo")
finally:
    try:
        categ.close()
    except Exception as e:
        print(f"no se pudo cerrar el archivo correctamente: {e}")



'''conversion de permisos'''
try:
    per = open(ruta_permisos, "r", encoding="utf-8")
    datos_permisos = json.load(per)
    roles_permisos = datos_permisos[0]
    permisos_disponibles = datos_permisos[1]
except:
    print("no se puede abrir el archivo")
finally:
    try:
        per.close()
    except Exception as e:
        print(f"no se pudo cerrar el archivo correctamente: {e}")



'''conversion de datos de usuarios'''
try:
    usu = open(ruta_usuarios, "r", encoding="utf-8")
    usuarios = json.load(usu)
except:
    print("no se puede abrir el archivo usuarios")
finally:
    try:
        usu.close()
    except Exception as e:
        print(f"no se pudo cerrar el archivo usuarios correctamente: {e}")




