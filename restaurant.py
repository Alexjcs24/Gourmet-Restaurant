#!/usr/bin/env python3
# restaurant.py
# Logica de gestion del restaurante y pedidos

import os
from menu import PLATOS

# Estructura del pedido actual: lista de diccionarios
# cada elemento: {"codigo": str, "nombre": str, "precio": float, "cantidad": int, "subtotal": float}
orden_actual = []


def agregar_producto(codigo, cantidad):
    """Agrega un producto y su cantidad a la orden."""
    if codigo not in PLATOS:
        return False, "El código ingresado no existe en la carta."

    if cantidad <= 0:
        return False, "La cantidad debe ser mayor a cero."

    plato = PLATOS[codigo]
    subtotal = plato["precio"] * cantidad

    # Si ya esta en la orden, sumamos la cantidad
    for item in orden_actual:
        if item["codigo"] == codigo:
            item["cantidad"] += cantidad
            item["subtotal"] += subtotal
            return True, f"Se agregaron {cantidad} unidad(es) más de {plato['nombre']}."

    # Si es nuevo en la orden
    orden_actual.append({
        "codigo": codigo,
        "nombre": plato["nombre"],
        "precio": plato["precio"],
        "cantidad": cantidad,
        "subtotal": subtotal
    })
    return True, f"¡{plato['nombre']} agregado exitosamente a la orden!"


def ver_orden():
    """Muestra el estado actual del carrito de compras."""
    if not orden_actual:
        print("\n--- La orden está vacía actualmente. ---")
        return 0, 0, 0

    print("\n" + "=" * 55)
    print("               ORDEN ACTUAL              ")
    print("=" * 55)
    print(f"{'Cant':<6}{'Descripción':<26}{'V. Unit':>10}{'Subtotal':>12}")
    print("-" * 55)

    subtotal_general = 0
    for item in orden_actual:
        precio_u_fmt = f"${item['precio']:,}".replace(",", ".")
        subtot_fmt = f"${item['subtotal']:,}".replace(",", ".")
        print(f"{item['cantidad']:<6}{item['nombre']:<26}{precio_u_fmt:>10}{subtot_fmt:>12}")
        subtotal_general += item["subtotal"]

    iva = subtotal_general * 0.08  # 8% impuesto al consumo para restaurantes
    total = subtotal_general + iva

    print("-" * 55)
    print(f"{'SUBTOTAL:':<42} {f'${int(subtotal_general):,}'.replace(',', '.'):>12}")
    print(f"{'IMPOCONSUMO (8%):':<42} {f'${int(iva):,}'.replace(',', '.'):>12}")
    print(f"{'TOTAL A PAGAR:':<42} {f'${int(total):,}'.replace(',', '.'):>12}")
    print("=" * 55)

    return subtotal_general, iva, total


def cancelar_orden():
    """Limpia la orden actual."""
    orden_actual.clear()
    print("\nOrden cancelada y reiniciada.")


def generar_factura(nombre_cliente="Consumidor Final"):
    """Genera la factura final en pantalla y guarda copia en archivo de texto."""
    if not orden_actual:
        print("\nNo hay productos en la orden para facturar.")
        return False

    subtotal, iva, total = ver_orden()

    factura_txt = []
    factura_txt.append("=======================================================")
    factura_txt.append("                 RESTAURANTE GOURMET                   ")
    factura_txt.append("                  NIT: 900.123.456-7                   ")
    factura_txt.append(f" Cliente: {nombre_cliente}")
    factura_txt.append("-------------------------------------------------------")
    factura_txt.append(f"{'Cant':<6}{'Descripción':<26}{'V. Unit':>10}{'Subtotal':>12}")
    factura_txt.append("-------------------------------------------------------")

    for item in orden_actual:
        precio_u_fmt = f"${item['precio']:,}".replace(",", ".")
        subtot_fmt = f"${item['subtotal']:,}".replace(",", ".")
        factura_txt.append(f"{item['cantidad']:<6}{item['nombre']:<26}{precio_u_fmt:>10}{subtot_fmt:>12}")

    factura_txt.append("-------------------------------------------------------")
    factura_txt.append(f"{'SUBTOTAL:':<42} {f'${int(subtotal):,}'.replace(',', '.'):>12}")
    factura_txt.append(f"{'IMPOCONSUMO (8%):':<42} {f'${int(iva):,}'.replace(',', '.'):>12}")
    factura_txt.append(f"{'TOTAL A PAGAR:':<42} {f'${int(total):,}'.replace(',', '.'):>12}")
    factura_txt.append("=======================================================")
    factura_txt.append("        ¡Gracias por su visita, vuelva pronto!         ")

    contenido = "\n".join(factura_txt)

    # Guardar en archivo para respaldo universitario
    try:
        ruta_factura = os.path.join(os.path.dirname(__file__), "factura_venta.txt")
        with open(ruta_factura, "w", encoding="utf-8") as f:
            f.write(contenido)
        print(f"\nFactura generada y guardada exitosamente en '{ruta_factura}'.")
    except Exception as e:
        print(f"\nNota: Factura generada (no se pudo escribir archivo: {e})")

    # Persistencia en PostgreSQL si el modulo esta disponible
    try:
        import crud_restaurante as cr
        if cr.esta_conectado():
            id_ped = cr.guardar_pedido_bd(nombre_cliente, orden_actual, subtotal, iva, total)
            if id_ped:
                print(f"[PostgreSQL] Pedido registrado en la base de datos con ID #{id_ped}.")
            else:
                print("[AVISO] La factura se generó en archivo, pero no pudo registrarse en PostgreSQL.")
        else:
            print("[MODO LOCAL] Factura emitida sin persistencia en base de datos (PostgreSQL no conectado).")
    except Exception as e:
        print(f"[AVISO BD] Error al intentar guardar en base de datos: {e}")

    # Limpiar orden luego de pagar
    orden_actual.clear()
    return True
