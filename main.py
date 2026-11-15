#!/usr/bin/env python3
# main.py
# NOMBRES DE LOS INTEGRANTES DEL PROYECTO:
# JESUS ESTEBAN MUNOZ GOMEZ
# ALBEIRO ANDRES RODGERS PEREZ
# ALEX JAVIER CAMPO SUAREZ

import titles as t
import menu as m
import restaurant as rt
import crud_restaurante as cr


def menu_pedidos_categoria(categoria_nombre):
    """Muestra los platos de una categoria y permite seleccionar plato y cantidad."""
    disponibles = m.mostrar_categoria(categoria_nombre)
    if not disponibles:
        input("\nPresione ENTER para volver al Menú Principal...")
        return

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


def menu_administrador():
    """Submenú de Gestión y Operaciones CRUD con la base de datos PostgreSQL."""
    while True:
        t.limpiar_pantalla()
        print("=" * 50)
        print("    PANEL DE ADMINISTRACIÓN Y BASE DE DATOS    ")
        print("=" * 50)
        estado_bd = cr.obtener_estado_conexion()
        print(f" Estado: [{estado_bd}]")
        print("-" * 50)
        print("1. Registrar nuevo plato (INSERT)")
        print("2. Consultar plato específico (SELECT)")
        print("3. Consultar todos los platos en PostgreSQL (SELECT)")
        print("4. Actualizar información de un plato (UPDATE)")
        print("5. Retirar plato de la carta (DELETE)")
        print("6. Reintentar conexión a PostgreSQL")
        print("0. Volver al Menú Principal")
        print("=" * 50)

        op = input("Seleccione una opción (0-6): ").strip()
        if op == "1":
            cr.registrar_plato()
            input("\nPresione ENTER para continuar...")
        elif op == "2":
            cr.consultar_plato()
            input("\nPresione ENTER para continuar...")
        elif op == "3":
            cr.consulta_todos_platos()
            input("\nPresione ENTER para continuar...")
        elif op == "4":
            cr.actualiza_plato()
            input("\nPresione ENTER para continuar...")
        elif op == "5":
            cr.eliminar_plato()
            input("\nPresione ENTER para continuar...")
        elif op == "6":
            cr.conectar_bd()
            if cr.esta_conectado():
                cr.sincronizar_con_menu()
                print("¡Conectado exitosamente y menú sincronizado con la base de datos!")
            else:
                print("No se pudo conectar a PostgreSQL.")
            input("\nPresione ENTER para continuar...")
        elif op == "0":
            break
        else:
            print("Opción no válida.")
            input("\nPresione ENTER para continuar...")


def main():
    # Establecer conexion con PostgreSQL (con autodeteccion y respaldo local si no esta disponible)
    conectado = cr.conectar_bd()
    if conectado:
        cr.sincronizar_con_menu()

    t.limpiar_pantalla()
    t.banner_bienvenida()

    # Confirmacion de ingreso al sistema
    ingresar = input("¿Deseas ingresar a nuestro menú? (s/n): ").strip().lower()
    if ingresar != "s":
        print("\nGracias por visitarnos. ¡Hasta pronto!")
        return

    while True:
        estado_bd = cr.obtener_estado_conexion()
        print("\n" + "=" * 45)
        print("             MENÚ PRINCIPAL            ")
        print(f"       [{estado_bd}]")
        print("=" * 45)
        print("1. Menú de Desayunos")
        print("2. Menú de Almuerzos")
        print("3. Menú de Postres")
        print("4. Ver Orden y Total")
        print("5. Confirmar Pedido y Facturar")
        print("6. Cancelar Orden Actual")
        print("7. Panel de Base de Datos y CRUD (Admin)")
        print("0. Salir del Sistema")
        print("=" * 45)

        opcion = input("Seleccione una opción (0-7): ").strip()

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
            case "7":
                menu_administrador()
            case "0":
                cr.terminar()
                print("\n¡Gracias por preferir Restaurante Gourmet! Que tenga un feliz día.")
                break
            case _:
                print("\nOpción no válida. Por favor elija un número entre 0 y 7.")


if __name__ == "__main__":
    main()
