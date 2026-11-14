#!/usr/bin/env python3
# crud_restaurante.py
# Modulo de funciones CRUD adaptado directamente del modelo explicado por el docente.
# PROYECTO INTEGRADOR ABP - FASE 3
# Integrantes:
#   - Jesus Esteban Munoz Gomez
#   - Albeiro Andres Rodgers Perez
#   - Alex Javier Campo Suarez

import psycopg2 as p

# Variable global de conexion, tal como la explico el docente
conexion = None


def conectar_bd(*paramconex):
    """Establece la conexion global con PostgreSQL."""
    try:
        global conexion
        conexion = p.connect(
            dbname=paramconex[0],
            user=paramconex[1],
            password=paramconex[2],
            host=paramconex[3],
            port=paramconex[4]
        )
        return True
    except Exception as e:
        # Fallback a conexion local socket si no hay contraseña configurada
        try:
            conexion = p.connect(dbname=paramconex[0], user=paramconex[1])
            return True
        except Exception:
            return False


def registrar_plato():
    """INSERT: Registra un nuevo plato en la base de datos."""
    print("\n" + "-" * 40)
    print("        REGISTRAR NUEVO PLATO          ")
    print("-" * 40)
    cursor = conexion.cursor()
    try:
        cod = input("Ingrese el código del plato: ").strip()
        nom = input("Ingrese el nombre del plato: ").strip()
        precio = float(input("Ingrese el precio del plato: ").strip())
        desc = input("Ingrese la descripción del plato: ").strip()
        print("Categorías disponibles: 1-Desayuno, 2-Almuerzo, 3-Postre")
        cat = int(input("Seleccione el ID de categoría (1-3): ").strip())

        ordensql = "INSERT INTO platos (codigo, nombre, precio, descripcion, id_categoria) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(ordensql, (cod, nom, precio, desc, cat))
        conexion.commit()
        print("-" * 40)
        print("¡Plato registrado exitosamente en la base de datos!")
    except Exception as e:
        conexion.rollback()
        print(f"Error al registrar plato: {e}")
    finally:
        cursor.close()


def consultaxplato():
    """SELECT INDIVIDUAL: Consulta un plato específico por su código."""
    print("\n" + "-" * 40)
    print("      CONSULTA DE PLATO ESPECÍFICO     ")
    print("-" * 40)
    cod = input("Ingrese el código del plato a consultar: ").strip()
    cursor = conexion.cursor()
    try:
        ordensql = """
            SELECT p.codigo, p.nombre, p.precio, c.nombre, p.descripcion
            FROM platos p
            JOIN categorias c ON p.id_categoria = c.id_categoria
            WHERE p.codigo = %s AND p.disponible = TRUE
        """
        cursor.execute(ordensql, (cod,))
        plato = cursor.fetchone()
        print("-" * 40)
        if plato:
            precio_fmt = f"${int(plato[2]):,}".replace(",", ".")
            print(f"Código:      {plato[0]}")
            print(f"Nombre:      {plato[1]}")
            print(f"Precio:      {precio_fmt}")
            print(f"Categoría:   {plato[3]}")
            print(f"Descripción: {plato[4]}")
        else:
            print("No se encontró ningún plato con ese código.")
        print("-" * 40)
    except Exception as e:
        print(f"Error al consultar: {e}")
    finally:
        cursor.close()


def consulta_todos_platos():
    """SELECT GENERAL: Lista todos los platos almacenados en la base de datos."""
    print("\n" + "=" * 60)
    print("         LISTADO GENERAL DE PLATOS EN POSTGRESQL        ")
    print("=" * 60)
    cursor = conexion.cursor()
    try:
        ordensql = """
            SELECT p.codigo, p.nombre, p.precio, c.nombre
            FROM platos p
            JOIN categorias c ON p.id_categoria = c.id_categoria
            WHERE p.disponible = TRUE
            ORDER BY CAST(p.codigo AS INTEGER) ASC
        """
        cursor.execute(ordensql)
        platos = cursor.fetchall()
        print(f"{'CÓD':<6}{'NOMBRE DEL PLATO':<30}{'CATEGORÍA':<14}{'PRECIO':>10}")
        print("-" * 60)
        for p_item in platos:
            precio_fmt = f"${int(p_item[2]):,}".replace(",", ".")
            print(f"{p_item[0]:<6}{p_item[1]:<30}{p_item[3]:<14}{precio_fmt:>10}")
        print("=" * 60)
    except Exception as e:
        print(f"Error al listar platos: {e}")
    finally:
        cursor.close()


def actualiza_plato():
    """UPDATE: Actualiza el precio o el nombre de un plato en la base de datos."""
    print("\n" + "-" * 40)
    print("          ACTUALIZANDO PLATO           ")
    print("-" * 40)
    cod = input("Ingrese el código del plato a actualizar: ").strip()
    cursor = conexion.cursor()
    try:
        campo = int(input("Ingrese el dato a actualizar (1-Nombre, 2-Precio): ").strip())
        if campo == 1:
            nuevo_nombre = input("Ingrese el nuevo nombre del plato: ").strip()
            ordensql = "UPDATE platos SET nombre = %s WHERE codigo = %s"
            cursor.execute(ordensql, (nuevo_nombre, cod))
        elif campo == 2:
            nuevo_precio = float(input("Ingrese el nuevo precio del plato: ").strip())
            ordensql = "UPDATE platos SET precio = %s WHERE codigo = %s"
            cursor.execute(ordensql, (nuevo_precio, cod))
        else:
            print("Opción no válida.")
            return

        conexion.commit()
        print("-" * 40)
        print("¡Plato actualizado con éxito en la base de datos!")
    except Exception as e:
        conexion.rollback()
        print(f"Error al actualizar: {e}")
    finally:
        cursor.close()


def deletplato():
    """DELETE: Da de baja un plato en la base de datos."""
    print("\n" + "-" * 40)
    print("           BORRANDO PLATO              ")
    print("-" * 40)
    cod = input("Ingrese el código del plato a retirar/borrar: ").strip()
    cursor = conexion.cursor()
    try:
        # Usamos disponible = FALSE para conservar consistencia de auditoria
        ordensql = "UPDATE platos SET disponible = FALSE WHERE codigo = %s"
        cursor.execute(ordensql, (cod,))
        conexion.commit()
        print("-" * 40)
        print("¡Plato retirado/borrado exitosamente de la base de datos!")
    except Exception as e:
        conexion.rollback()
        print(f"Error al borrar plato: {e}")
    finally:
        cursor.close()


def guardar_pedido_bd(cliente, orden, subtotal, impoconsumo, total):
    """Inserta el pedido y su detalle en PostgreSQL."""
    if not conexion:
        return None
    cursor = conexion.cursor()
    try:
        ordensql_pedido = """
            INSERT INTO pedidos (cliente, subtotal, impoconsumo, total, estado)
            VALUES (%s, %s, %s, %s, 'PAGADO')
            RETURNING id_pedido;
        """
        cursor.execute(ordensql_pedido, (cliente, subtotal, impoconsumo, total))
        id_pedido = cursor.fetchone()[0]

        ordensql_detalle = """
            INSERT INTO detalle_pedidos (id_pedido, codigo_plato, cantidad, precio_unitario, subtotal_linea)
            VALUES (%s, %s, %s, %s, %s);
        """
        for item in orden:
            cursor.execute(ordensql_detalle, (
                id_pedido,
                item["codigo"],
                item["cantidad"],
                item["precio"],
                item["subtotal"]
            ))

        conexion.commit()
        return id_pedido
    except Exception as e:
        conexion.rollback()
        print(f"[BD] Error al guardar pedido: {e}")
        return None
    finally:
        cursor.close()


def terminar():
    """Cierra la conexion con la base de datos."""
    global conexion
    if conexion:
        conexion.close()
        print("Conexión con PostgreSQL cerrada.")
