#!/usr/bin/env python3
# titles.py
# Modulo con los encabezados y titulos del restaurante

def limpiar_pantalla():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def banner_bienvenida():
    print("=" * 45)
    print("        RESTAURANTE GOURMET        ")
    print("  ¡Bienvenidos a nuestro restaurante!  ")
    print("=" * 45)


def breakfast_menu():
    print("\n" + "=" * 40)
    print("            DESAYUNOS            ")
    print("=" * 40)


def midfood_menu():
    print("\n" + "=" * 40)
    print("            ALMUERZOS            ")
    print("=" * 40)


def desserts_menu():
    print("\n" + "=" * 40)
    print("             POSTRES             ")
    print("=" * 40)


def factura_header():
    print("\n" + "=" * 45)
    print("         RESUMEN DE FACTURA          ")
    print("=" * 45)
