# HAY QUE RENOMBRAR ESTE A MAIN

# Funciones Rich
from Menus.menus import *
from Datos.Datos import (
    gastos,
    presupuestos,
    categoria,
    encabezadosC,
    encabezadosG,
    encabezadosP
)
# -- FUNCIONES RICH

# Desde Func.Func_Rich

# --FUNCIONES DE VALIDACION

# Desde Func.Auxiliares

# -- FUNCIONES MATRICES

# Desde Func.Func_Matriz 

# CRUD CATEGORIAS

# Desde Crud.Crud_Cat

## CRUD PRESUPUESTOS

# Desde Crud.Crud_Pres

# CRUD GASTOS

# Desde Crud.Crud_Gast

def main():
    menu_principal(categoria,presupuestos,gastos,encabezadosC,encabezadosP,encabezadosG)


if __name__ == "__main__":
    main()