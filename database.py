#!/usr/bin/env python3
# database.py
# Modulo adaptador y fachada de base de datos
# Redirige al modulo unificado crud_restaurante.py para mantener compatibilidad total.
# PROYECTO INTEGRADOR ABP - FASE 3
# Integrantes:
#   - Jesus Esteban Munoz Gomez
#   - Albeiro Andres Rodgers Perez
#   - Alex Javier Campo Suarez

import crud_restaurante as cr


def conectar_bd(*args, **kwargs):
    """Establece conexión con PostgreSQL."""
    return cr.conectar_bd(*args, **kwargs)


def obtener_catalogo_platos():
    """Consulta los platos disponibles en BD."""
    return cr.obtener_catalogo_bd() or {}


def registrar_pedido(cliente, orden, subtotal, impoconsumo, total):
    """Registra un pedido en PostgreSQL."""
    return cr.guardar_pedido_bd(cliente, orden, subtotal, impoconsumo, total)


def actualizar_precio_plato(codigo, nuevo_precio):
    """Actualiza el precio de un plato."""
    if not cr.esta_conectado():
        return False, "Sin conexión a base de datos."
    cur = cr.conexion.cursor()
    try:
        cur.execute("UPDATE platos SET precio = %s WHERE codigo = %s", (nuevo_precio, codigo))
        filas = cur.rowcount
        if filas > 0:
            cr.conexion.commit()
            cr.sincronizar_con_menu()
            return True, f"Precio del plato {codigo} actualizado a ${nuevo_precio}."
        else:
            cr.conexion.rollback()
            return False, f"No se encontró el plato con código {codigo}."
    except Exception as e:
        cr.conexion.rollback()
        return False, f"Error: {e}"
    finally:
        cur.close()


def eliminar_plato(codigo):
    """Retira un plato de la carta."""
    if not cr.esta_conectado():
        return False, "Sin conexión a base de datos."
    cur = cr.conexion.cursor()
    try:
        cur.execute("UPDATE platos SET disponible = FALSE WHERE codigo = %s AND disponible = TRUE", (codigo,))
        filas = cur.rowcount
        if filas > 0:
            cr.conexion.commit()
            cr.sincronizar_con_menu()
            return True, f"Plato {codigo} retirado."
        else:
            cr.conexion.rollback()
            return False, f"No se encontró el plato activo con código {codigo}."
    except Exception as e:
        cr.conexion.rollback()
        return False, f"Error: {e}"
    finally:
        cur.close()
