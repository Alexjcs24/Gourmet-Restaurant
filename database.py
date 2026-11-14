#!/usr/bin/env python3
# database.py
# Modulo de conexion y operaciones CRUD con PostgreSQL
# PROYECTO INTEGRADOR ABP - FASE 3
# Integrantes:
#   - Jesus Esteban Munoz Gomez
#   - Albeiro Andres Rodgers Perez
#   - Alex Javier Campo Suarez

import psycopg2
from psycopg2 import extras

# Parametros de conexion por defecto a PostgreSQL local
DB_CONFIG = {
    "dbname": "restaurante_gourmet",
    "user": "alexcs"
}



def conectar_bd():
    """Establece y retorna una conexion con la base de datos PostgreSQL.
    Retorna None si ocurre un error de conexion."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as err:
        print(f"\n[ERROR BD] No se pudo conectar a PostgreSQL: {err}")
        return None


def obtener_catalogo_platos():
    """Consulta (SELECT) todos los platos disponibles en la base de datos junto con su categoria.
    Retorna un diccionario estructurado identico a PLATOS."""
    conn = conectar_bd()
    if not conn:
        return {}

    platos_dict = {}
    query = """
        SELECT p.codigo, p.nombre, p.precio, p.descripcion, c.nombre AS categoria
        FROM platos p
        INNER JOIN categorias c ON p.id_categoria = c.id_categoria
        WHERE p.disponible = TRUE
        ORDER BY CAST(p.codigo AS INTEGER) ASC;
    """
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(query)
            filas = cur.fetchall()
            for fila in filas:
                platos_dict[str(fila["codigo"])] = {
                    "nombre": fila["nombre"],
                    "precio": float(fila["precio"]),
                    "descripcion": fila["descripcion"] or "",
                    "categoria": fila["categoria"]
                }
    except psycopg2.Error as err:
        print(f"[ERROR BD] Fallo al consultar platos: {err}")
    finally:
        conn.close()

    return platos_dict


def registrar_pedido(cliente, orden, subtotal, impoconsumo, total):
    """Inserta (INSERT) un nuevo pedido y sus detalles en la base de datos.
    Retorna el id_pedido generado o None si falla."""
    conn = conectar_bd()
    if not conn:
        return None

    try:
        with conn.cursor() as cur:
            # 1. Insertar en tabla pedidos
            query_pedido = """
                INSERT INTO pedidos (cliente, subtotal, impoconsumo, total, estado)
                VALUES (%s, %s, %s, %s, 'PAGADO')
                RETURNING id_pedido;
            """
            cur.execute(query_pedido, (cliente, subtotal, impoconsumo, total))
            id_pedido = cur.fetchone()[0]

            # 2. Insertar cada producto en detalle_pedidos
            query_detalle = """
                INSERT INTO detalle_pedidos (id_pedido, codigo_plato, cantidad, precio_unitario, subtotal_linea)
                VALUES (%s, %s, %s, %s, %s);
            """
            for item in orden:
                cur.execute(query_detalle, (
                    id_pedido,
                    item["codigo"],
                    item["cantidad"],
                    item["precio"],
                    item["subtotal"]
                ))

        conn.commit()
        return id_pedido
    except psycopg2.Error as err:
        conn.rollback()
        print(f"[ERROR BD] No se pudo registrar el pedido: {err}")
        return None
    finally:
        conn.close()


def consultar_pedido(id_pedido):
    """Consulta (SELECT) la informacion de un pedido y sus detalles por id."""
    conn = conectar_bd()
    if not conn:
        return None

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM pedidos WHERE id_pedido = %s;", (id_pedido,))
            pedido = cur.fetchone()
            if not pedido:
                return None

            cur.execute("""
                SELECT d.*, p.nombre 
                FROM detalle_pedidos d
                JOIN platos p ON d.codigo_plato = p.codigo
                WHERE d.id_pedido = %s;
            """, (id_pedido,))
            detalles = cur.fetchall()
            return dict(pedido), [dict(d) for d in detalles]
    except psycopg2.Error as err:
        print(f"[ERROR BD] Fallo al consultar el pedido {id_pedido}: {err}")
        return None
    finally:
        conn.close()


def actualizar_precio_plato(codigo, nuevo_precio):
    """Actualiza (UPDATE) el precio de un plato en la base de datos."""
    conn = conectar_bd()
    if not conn:
        return False, "Sin conexión a base de datos."

    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE platos
                SET precio = %s
                WHERE codigo = %s;
            """, (nuevo_precio, codigo))
            actualizados = cur.rowcount
        conn.commit()
        if actualizados > 0:
            return True, f"Precio del plato {codigo} actualizado a ${nuevo_precio:,.0f}."
        else:
            return False, f"No se encontró el plato con código {codigo}."
    except psycopg2.Error as err:
        conn.rollback()
        return False, f"Error al actualizar precio: {err}"
    finally:
        conn.close()


def eliminar_plato(codigo):
    """Marca como no disponible o elimina (DELETE) un plato de la carta."""
    conn = conectar_bd()
    if not conn:
        return False, "Sin conexión a base de datos."

    try:
        with conn.cursor() as cur:
            # Primero intentamos borrado logico (disponible = FALSE) para no romper pedidos historicos
            cur.execute("""
                UPDATE platos
                SET disponible = FALSE
                WHERE codigo = %s;
            """, (codigo,))
            actualizados = cur.rowcount
        conn.commit()
        if actualizados > 0:
            return True, f"Plato con código {codigo} retirado de la carta."
        else:
            return False, f"No se encontró el plato {codigo}."
    except psycopg2.Error as err:
        conn.rollback()
        return False, f"Error al eliminar plato: {err}"
    finally:
        conn.close()
