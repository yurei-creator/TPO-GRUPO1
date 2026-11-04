import json

ruta_encabezadoC = "Datos/encabezadosC.json"
ruta_encabezadoG = "Datos/encabezadosG.json"
ruta_encabezadoP = "Datos/encabezadosP.json"
ruta_categoria = "Datos/categorias.json"
ruta_gastos = "Datos/gastos.json"
ruta_presupuestos = "Datos/presupuestos.json"
ruta_permisos = "Datos/permisos.json"
ruta_roles_permisos = "Datos/roles_permisos.json"
ruta_usuarios = "Datos/datos_usuarios.json"

rutas = [ruta_encabezadoC, 
         ruta_encabezadoG, 
         ruta_encabezadoP, 
         ruta_categoria, 
         ruta_gastos,
         ruta_presupuestos,
         ruta_permisos,
         ruta_roles_permisos,
         ruta_usuarios]

"Conversion a python"

def conversion_a_python(archivo):
    try:
        ruta = open(archivo, "r", encoding="utf-8")
        conversion = json.loads(ruta)
        
    except:
        print("no se puede abrir el archivo")
    finally:
        try:
            ruta.close()
        except Exception as e:
            print(f"no se pudo cerrar el archivo correctamente: {e}")
    return conversion

"Conversion a Json"

def conversion_a_json(informacion):
    ruta_json = json.dumps(informacion)
    return ruta_json


for i in range(len(rutas)):
    rutas[i] = conversion_a_python[i]

encabezadoC = rutas[0]
encabezadoP = rutas[1]
encabezadoG = rutas[2]
categorias = rutas[3]
gastos = rutas[4]
presupuestos = rutas[5]
permisos = rutas[6]
PERMISOS_DISPONIBLES = rutas[7]
usuarios = rutas[8]




