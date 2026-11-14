#!/usr/bin/env python3
# main.py
# NOMBRES DE LOS INTEGRANTES DEL PROYECTO:
# JESUS ESTEBAN MUNOZ GOMEZ
# ALBEIRO ANDRES RODGERS PEREZ
# ALEX JAVIER CAMPO SUAREZ

import titles as t
import menu as m
import restaurant as rt


def menu_pedidos_categoria(categoria_nombre):
    """Muestra los platos de una categoria y permite seleccionar plato y cantidad."""
    m.mostrar_categoria(categoria_nombre)
    while True:
        cod = input("\nIngrese el código del plato que desea agregar (o 0 para volver): ").strip()
        if cod == "0":
            break

        if cod not in m.PLATOS or m.PLATOS[cod]["categoria"] != categoria_nombre:
            print("Código no válido para esta categoría. Intente nuevamente.")
            continue

        plato_sel = m.PLATOS[cod]
        print(f"Ha seleccionado: {plato_sel['nombre']} (${plato_sel['precio']:,})".replace(",", "."))
        
        try:
            cant = int(input("Ingrese la cantidad que desea: ").strip())
            if cant <= 0:
                print("La cantidad debe ser mayor a 0.")
                continue
        except ValueError:
            print("Por favor ingrese un número entero válido.")
            continue

        exito, msg = rt.agregar_producto(cod, cant)
        print(f"\n>> {msg}")

        seguir = input("¿Desea agregar otro plato de esta sección? (s/n): ").strip().lower()
        if seguir != "s":
            break


def main():
    t.limpiar_pantalla()
    t.banner_bienvenida()

    # Confirmacion de ingreso al sistema
    ingresar = input("¿Deseas ingresar a nuestro menú? (s/n): ").strip().lower()
    if ingresar != "s":
        print("\nGracias por visitarnos. ¡Hasta pronto!")
        return

    while True:
        print("\n" + "=" * 45)
        print("             MENÚ PRINCIPAL            ")
        print("=" * 45)
        print("1. Menú de Desayunos")
        print("2. Menú de Almuerzos")
        print("3. Menú de Postres")
        print("4. Ver Orden y Total")
        print("5. Confirmar Pedido y Facturar")
        print("6. Cancelar Orden Actual")
        print("0. Salir del Sistema")
        print("=" * 45)

        opcion = input("Seleccione una opción (0-6): ").strip()

        match opcion:
            case "1":
                t.limpiar_pantalla()
                menu_pedidos_categoria("Desayuno")
            case "2":
                t.limpiar_pantalla()
                menu_pedidos_categoria("Almuerzo")
            case "3":
                t.limpiar_pantalla()
                menu_pedidos_categoria("Postre")
            case "4":
                t.limpiar_pantalla()
                rt.ver_orden()
                input("\nPresione ENTER para continuar...")
            case "5":
                t.limpiar_pantalla()
                if not rt.orden_actual:
                    print("\nNo tiene platos en la orden para facturar.")
                    input("\nPresione ENTER para continuar...")
                else:
                    cliente = input("Ingrese el nombre del cliente: ").strip()
                    if not cliente:
                        cliente = "Consumidor Final"
                    rt.generar_factura(cliente)
                    input("\nPresione ENTER para continuar...")
            case "6":
                rt.cancelar_orden()
                input("\nPresione ENTER para continuar...")
            case "0":
                print("\n¡Gracias por preferir Restaurante Gourmet! Que tenga un feliz día.")
                break
            case _:
                print("\nOpción no válida. Por favor elija un número entre 0 y 6.")


if __name__ == "__main__":
    main()
