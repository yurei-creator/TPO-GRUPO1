# -----------------------------------------------------------------------------
# SISTEMA DE CONTROL DE GASTOS PERSONALES Y FAMILIARES
# Programación 1 - Algoritmos y Estructuras de Datos 1
# Trabajo Práctico Obligatorio - Primera Entrega
# -----------------------------------------------------------------------------

from Menus.menus import menu_principal
from Datos.Datos import (
    categoria,
    presupuestos,
    gastos,
    encabezadosC,
    encabezadosP,
    encabezadosG
)
from Crud.Crud_Usuarios import login

def main():
    usuario = login()
    if usuario:
        menu_principal(
            usuario,
            categoria,
            presupuestos,
            gastos,
            encabezadosC,
            encabezadosP,
            encabezadosG
        )

if __name__ == "__main__":
    main()