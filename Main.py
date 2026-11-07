# -----------------------------------------------------------------------------
# SISTEMA DE CONTROL DE GASTOS PERSONALES Y FAMILIARES
# Programación 1 - Algoritmos y Estructuras de Datos 1
# Trabajo Práctico Obligatorio - Segunda Entrega
# -----------------------------------------------------------------------------


from Menus.menus import menu_principal
from Datos.Datos import (
    presupuestos,
    encabezadosC,
    encabezadosP,
    encabezadosG
)

from Crud.Crud_Usuarios import login
from Crud.Crud_Gast import leer_gastos

def main():

    usuario = login()
    if usuario:
        menu_principal(
            usuario,
            presupuestos,
            leer_gastos(),
            encabezadosC,
            encabezadosP,
            encabezadosG
        )

if __name__ == "__main__":
    main()