#--------------------------LISTAS GASTOS--------------------------------------------#
NombreG = ["Supermercado", "Gasolina", "Cine", "Farmacia", "Curso online"]

MontoG = [120, 45, 25, 15.50, 80]

FechaG = ["01/08/2026", "02/08/2026", "03/08/2026", "04/08/2026", "05/08/2026"]

CategoriaG = ["Alimentos", "Transporte", "Ocio", "Salud", "Educación"]

DescripcionG = [
    "Compra mensual de viveres", 
    "Tanque lleno del auto", 
    "Entradas y palomitas", 
    "Medicamentos para la gripe", 
    "Inscripción a taller de Excel"
]
#--------------------------LISTAS PRESUPUESTOS--------------------------------------------#
NombreP = ["Limite Alimentos", "Limite Transporte", "Limite Ocio", "Limite Salud", "Limite Educación"]

MontoP = [400, 150, 100, 80, 120]

FechaP = ["01/08/2026", "01/08/2026", "01/08/2026", "01/08/2026", "01/08/2026"]

CategoriaP = ["Alimentos", "Transporte", "Ocio", "Salud", "Educación"]

DescripcionP = [
    "Presupuesto maximo del mes", 
    "Estimado para pasajes y gasolina", 
    "Dinero para salidas y diversion", 
    "Reservas para emergencias medicas", 
    "Libros y materiales de estudio"
]
# CREACION DE MATRICES 
CantFilas = 5
CantColumnas = 5
MatrizP = [[0]*CantColumnas for _ in range(CantFilas)]
MatrizG = [[0]*CantColumnas for _ in range(CantFilas)]
# LLENAR MATRICES
def llenar_matrizGastos(matriz):
    filas = len(matriz)
    columnas = len(matriz[0]) 
    for fil in range(filas):
        for col in range(columnas):
            if col == 0:
                matriz[fil][col] = NombreG[fil]
            elif col == 1:
                matriz[fil][col] = MontoG[fil]
            elif col == 2:
                matriz[fil][col] = FechaG[fil]
            elif col == 3:
                matriz[fil][col] = CategoriaG[fil]
            elif col == 4:
                matriz[fil][col] = DescripcionG[fil]
def llenar_matrizPresupuestos(matriz):
    filas = len(matriz)
    columnas = len(matriz[0]) 
    for fil in range(filas):
        for col in range(columnas):
            if col == 0:
                matriz[fil][col] = NombreP[fil]
            elif col == 1:
                matriz[fil][col] = MontoP[fil]
            elif col == 2:
                matriz[fil][col] = FechaP[fil]
            elif col == 3:
                matriz[fil][col] = CategoriaP[fil]
            elif col == 4:
                matriz[fil][col] = DescripcionP[fil]
# MOSTRAR MATRICES
def mostrar_matriz(encabezados, matriz):
    filas = len(matriz)
    columnas = len(matriz[0])
    anchos = []

    for col in range(columnas):
        ancho = len(encabezados[col])
        for fila in range(filas):
            valor = str(matriz[fila][col])
            if len(valor) > ancho:
                ancho = len(valor)
        anchos.append(ancho)

    for col in range(columnas):
        titulo = encabezados[col]
        espacios = " " * (anchos[col] - len(titulo))
        print(titulo + espacios + "  ", end="")
    print()

    for fila in range(filas):
        for col in range(columnas):
            valor = str(matriz[fila][col])
            espacios = " " * (anchos[col] - len(valor))
            print(valor + espacios + "  ", end="")  
        print()
# PROGRAMA PRINCIPAL
encabezadosG = ["Gastos", "Monto", "Fecha", "Categoria", "Descripcion"]
encabezadosP = ["Presupuestos", "Monto", "Fecha", "Categoria", "Descripcion"]

llenar_matrizGastos(MatrizG)
llenar_matrizPresupuestos(MatrizP)
mostrar_matriz(encabezadosG, MatrizG)
print()
print()
mostrar_matriz(encabezadosP, MatrizP)
