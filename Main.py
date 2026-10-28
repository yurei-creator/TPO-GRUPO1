# -----------------------------------------------------------------------------
# SISTEMA DE CONTROL DE GASTOS PERSONALES Y FAMILIARES
# Programación 1 - Algoritmos y Estructuras de Datos 1
# Trabajo Práctico Obligatorio - Primera Entrega
# -----------------------------------------------------------------------------

from Menus.menus import menu_principal
from Datos.Datos import (
    gastos,
    encabezadosC,
    encabezadosP,
    encabezadosG,
    cargar_presupuestos,
    cargar_categorias
)
from Crud.Crud_Usuarios import login

def main():
    usuario = login()
    if usuario:
        presupuestos = cargar_presupuestos()
        categorias =  cargar_categorias()
        menu_principal(
            usuario,
            categorias,
            presupuestos,
            gastos,
            encabezadosC,
            encabezadosP,
            encabezadosG
        )

if __name__ == "__main__":
    main()