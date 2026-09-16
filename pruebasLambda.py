from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from functools import reduce
from datosprincipales import (
    clave_login,
    Id_Categoria,
    gastos,
    datos_porcentaje,
    datos_infla,
    MontoG)
console = Console()


'''Login'''

def login(n1):
    info=n1
    usuario=input("Por favor ingrese su nombre de usuario:\n")
    clave=input("Por favor, ingrese su contraseña:\n")
    while usuario != info[0] or clave != info[1]:
        print("Error, usuario y/o clave incorrecta.")
        usuario=input("Por favor ingrese su nombre de usuario:\n")
        clave=input("Por favor, ingrese su contraseña:\n")



'''Creación de matrices'''

def matriz(n1):
    ordenar=[]
    cont=0
    while cont < len(n1):
        ordenar.append([])
        cont=cont+1
    return ordenar


'''Añadir valores a las listas de la matriz'''

def agregado(n1):
    datos=n1
    listas=matriz(datos[0])
    cont1=0
    while cont1 < len(listas):
        cont2=0
        while cont2 < len(datos):
            listas[cont1].append(datos[cont2][cont1])
            cont2= cont2 + 1 
        cont1= cont1 + 1
    return listas


'''Metodos de Ordenamientos en Lambda'''

def ordenamientos(n1):
    matrices=n1
    opcion=int(input("Por favor ingrese una opcion de orden:\nNombre(0).\nFecha(1).\nMonto(2).\nDescripción(3).\nPeriodo(4).\n:"))
    while opcion < 0 or opcion > 4:
        print("error, numero invalido")
        opcion=int(input("Por favor ingrese una opcion de orden:\nNombre(0).\nFecha(1).\nMonto(2).\nDescripción(3).\nPeriodo(4).\n:"))
    metodo=int(input("Por favor, ingrese 0 si quiere el orden de mayor a menor.\ningrese 1 si quiere el orden de menor a mayor.\n:"))
    while metodo < 0 or metodo > 1:
        print("error, numero invalido")
        metodo=int(input("Por favor, ingrese 0 si quiere el orden de mayor a menor.\ningrese 1 si quiere el orden de menor a mayor.\n:"))
    if metodo==0:
        orden_matrices=sorted(matrices, key=lambda dato: dato[opcion])
    else:orden_matrices=sorted(matrices, key=lambda dato: dato[opcion],reverse=True)
    return orden_matrices



'''Sumatoria de los Montos'''

def totaldegasto(n1):
    costes=n1
    nominal=reduce(lambda x, y: x + y, costes)
    total=str(nominal)+"$"
    return nominal,total



'''Precisión decimal'''

def grado():
    decimales=int(input("Por favor, ingrese el grado de precision decimal (estandar=2)."))
    while decimales < 0 or decimales > 15:
        print("Error, grado de precision invalido.")
        decimales=int(input("Por favor, ingrese el grado de precision decimal (estandar=2)."))
    return decimales



''' Porcentajes del total.'''

def estadistica(n1):
    nombres=n1[0]
    numerador=n1[1]
    listas_porcentaje=matriz(n1[0])
    monto_total=totaldegasto(n1[1])
    listas_numero=matriz(n1[0])
    precision=grado()
    cont=0
    while cont < len(n1[0]):
        porcentaje=round((lambda a, b, c: a * b / c)(numerador[cont], 100 ,monto_total[0]), precision)
        listas_numero[cont].append(porcentaje)
        cont=cont+1
    cont=0
    while cont < len(n1[0]):
        temporal=listas_numero[cont][0]
        temporal=str(temporal)+str(" %")
        auxiliar=nombres[cont]
        auxiliar=str(auxiliar)+str(": ")
        listas_porcentaje[cont]=auxiliar+temporal
        cont=cont+1
    return listas_porcentaje,precision


    
'''Porcentajes especificos'''

def especifico(n1):
    cont=0
    entrada=n1
    punto=[]
    cantidad=int(input("Por favor, ingrese la cantidad de valores que desea: "))
    while cantidad < 0 or cantidad > len(n1[1]):
        print("Error, cantidad invalida.")
        cantidad=int(input("Por favor, ingrese la cantidad de valores que desea: "))
    while cont < cantidad :
        num=int(input("Por favor ingrese un numero: "))
        while num <= 0 or num > len(entrada):
            print("Error, este numero es invalido.")
            num=int(input("Por favor ingrese un numero: "))
        punto.append(entrada[num-1])
        cont=cont+1
    return punto

    


'''Calculo de inflación y deflación'''

def inflacion(n1,n2):
    decimas=n2
    dicio=list(n1.values())
    plata=dicio[0][0]
    plata=list(plata)
    aux=[]
    cont=0
    modo=int(input("Desea calcular la inflación mensualmente(0) o anualmente(1): "))
    while modo != 0 and modo != 1:
        print("Error, el numero es invalido.")
        modo=int(input("Desea calcular la inflación mensualmente(0) o anualmente(1): "))
    periodo=int(input("Ingrese en forma numerica la cantidad de tiempo de meses/años:"))
    while periodo < 0 :
        print("Error, el numero es invalido.")
        periodo=int(input("Ingrese en forma numerica la cantidad de tiempo de meses/años:"))
    if modo == 1 :
        periodo=periodo/12
    infla_tasa=input("Ingrese su estimación numerica sobre la tasa de inflación(numero positivo)\no deflación(numero negativo): ")
    infla_tasa=float(infla_tasa)/100
    acumulado= (lambda a,b,c:((a+b)**c)-a)(1.0,infla_tasa,periodo)
    while cont < len(plata):
        aux=plata[cont]
        aux=float(aux)
        resultado= (lambda a,b: a+(a*b))(aux,acumulado)
        resultado=round(resultado,decimas)
        plata[cont]=resultado
        cont=cont+1
    return plata


'''Gastos por Categoria'''

def gas_cat(n1):
    informacion=n1
    cont1=0
    matriz_dato=agregado(informacion)
    matriz_categ=matriz(informacion[5])
    while cont1 < len(matriz_categ):
        matriz_categ[cont1].append(informacion[5][cont1])
        cont2=0
        while cont2 < len(matriz_dato):
            if matriz_dato[cont2][5] == matriz_categ[cont1][0]:
                matriz_categ[cont1].append(matriz_dato[cont2][2])
            cont2=cont2+1
        cont1=cont1+1
    return matriz_categ















'''Programa Principal'''

copia=datos_infla.copy()

login(clave_login)
creacion=matriz(gastos[0])
valores=agregado(gastos)
orden=ordenamientos(valores)
promedio=estadistica(datos_porcentaje)
puntual=especifico(promedio[0])
variacion=inflacion(copia,promedio[1])
monto_categoria=gas_cat(gastos)
print(creacion,"\n")
print(valores,"\n")
print(orden,"\n")
print(totaldegasto(MontoG)[1],"\n")
print(promedio[0],"\n")
print(puntual)
print(variacion)
print(monto_categoria)
