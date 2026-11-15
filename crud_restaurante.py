#!/usr/bin/env python3
# crud_restaurante.py
# Módulo de funciones CRUD y persistencia con PostgreSQL
# PROYECTO INTEGRADOR ABP - FASE 3
# Integrantes:
#   - Jesús Esteban Muñoz Gómez
#   - Albeiro Andrés Rodgers Pérez
#   - Alex Javier Campo Suárez

import os

# Import seguro de psycopg2 para evitar ModuleNotFoundError si no está instalado
try:
    import psycopg2 as p
    HAY_PSYCOPG2 = True
except ImportError:
    p = None
    HAY_PSYCOPG2 = False

# Variable global de conexión
conexion = None
motivo_desconexion = "No inicializado"


def esta_conectado():
    """Verifica si existe una conexión activa y válida a la base de datos."""
    if conexion is None:
        return False
    try:
        return conexion.closed == 0
    except Exception:
        return False


def obtener_estado_conexion():
    """Retorna una cadena descriptiva con el estado actual de la conexión."""
    if esta_conectado():
        return "PostgreSQL Conectado"
    if not HAY_PSYCOPG2:
        return "Modo Local (Falta psycopg2)"
    return f"Modo Local ({motivo_desconexion})"


def conectar_bd(dbname=None, user=None, password=None, host=None, port=None):
    """Establece la conexión global con PostgreSQL.
    Retorna True si conecta, o False si continúa en modo local."""
    global conexion, motivo_desconexion

    if not HAY_PSYCOPG2:
        motivo_desconexion = "Falta librería psycopg2"
        return False

    db = dbname or os.environ.get("DB_NAME", "restaurante_gourmet")
    # Soporte multiplataforma: USER (Linux/Mac) y USERNAME (Windows)
    usuario = user or os.environ.get("DB_USER") or os.environ.get("USER") or os.environ.get("USERNAME", "postgres")
    clave = password if password is not None else os.environ.get("DB_PASSWORD", "")
    servidor = host or os.environ.get("DB_HOST", "localhost")
    puerto = port or os.environ.get("DB_PORT", "5432")

    # 1. Intentar con parámetros especificados o variables de entorno
    try:
        conexion = p.connect(dbname=db, user=usuario, password=clave, host=servidor, port=puerto)
        motivo_desconexion = ""
        return True
    except Exception as e:
        motivo_desconexion = "PostgreSQL no disponible o credenciales inválidas"

    # 2. Intento de respaldo estándar (usuario del sistema o postgres local)
    try:
        conexion = p.connect(dbname=db, user=usuario)
        motivo_desconexion = ""
        return True
    except Exception:
        pass

    try:
        conexion = p.connect(dbname=db, user="postgres")
        motivo_desconexion = ""
        return True
    except Exception:
        pass

    return False


def pedir_datos_plato():
    """Pide y valida interactivamente los datos de un plato (nombre, precio, descripcion, categoria)."""
    nom = input("Ingrese el nombre del plato: ").strip()
    if not nom:
        print("El nombre no puede estar vacío.")
        return None

    try:
        precio = float(input("Ingrese el precio del plato: ").strip())
        if precio <= 0:
            print("El precio debe ser mayor a 0.")
            return None
    except ValueError:
        print("El precio debe ser un número válido.")
        return None

    desc = input("Ingrese la descripción del plato: ").strip()
    print("Categorías disponibles: 1-Desayuno, 2-Almuerzo, 3-Postre")
    try:
        cat = int(input("Seleccione el ID de categoría (1-3): ").strip())
        if cat not in [1, 2, 3]:
            print("Categoría no válida. Debe ser 1, 2 o 3.")
            return None
    except ValueError:
        print("Debe ingresar un número entero (1, 2 o 3).")
        return None

    return nom, precio, desc, cat


def registrar_plato():
    """INSERT: Registra un nuevo plato en la base de datos o reactiva uno retirado."""
    if not esta_conectado():
        print("\n[ERROR BD] No hay conexión activa a la base de datos PostgreSQL.")
        return False

    print("\n" + "-" * 40)
    print("        REGISTRAR NUEVO PLATO          ")
    print("-" * 40)
    cursor = conexion.cursor()
    try:
        cod = input("Ingrese el código del plato: ").strip()
        if not cod:
            print("El código no puede estar vacío.")
            return False

        # Verificar si el código ya existe
        cursor.execute("SELECT codigo, disponible, nombre FROM platos WHERE codigo = %s", (cod,))
        existente = cursor.fetchone()

        if existente:
            if not existente[1]:  # Está retirado
                reactivar = input(f"El plato '{existente[2]}' existe pero está retirado. ¿Desea reactivarlo y actualizarlo? (s/n): ").strip().lower()
                if reactivar == 's':
                    datos = pedir_datos_plato()
                    if not datos:
                        return False
                    nom, precio, desc, cat = datos
                    cursor.execute("""
                        UPDATE platos 
                        SET nombre = %s, precio = %s, descripcion = %s, id_categoria = %s, disponible = TRUE 
                        WHERE codigo = %s
                    """, (nom, precio, desc, cat, cod))
                    conexion.commit()
                    sincronizar_con_menu()
                    print("-" * 40)
                    print(f"¡Plato '{nom}' (Cód: {cod}) reactivado y actualizado exitosamente!")
                    return True
                else:
                    return False
            else:
                print(f"Error: Ya existe un plato activo con el código '{cod}' ('{existente[2]}').")
                return False

        # Si es un plato nuevo
        datos = pedir_datos_plato()
        if not datos:
            return False
        nom, precio, desc, cat = datos

        ordensql = """
            INSERT INTO platos (codigo, nombre, precio, descripcion, id_categoria, disponible) 
            VALUES (%s, %s, %s, %s, %s, TRUE)
        """
        cursor.execute(ordensql, (cod, nom, precio, desc, cat))
        conexion.commit()
        sincronizar_con_menu()
        print("-" * 40)
        print(f"¡Plato '{nom}' registrado exitosamente en la base de datos!")
        return True
    except Exception as e:
        conexion.rollback()
        print(f"Error al registrar plato: {e}")
        return False
    finally:
        cursor.close()


def consultar_plato():
    """SELECT INDIVIDUAL: Consulta un plato específico por su código."""
    if not esta_conectado():
        print("\n[ERROR BD] No hay conexión activa a la base de datos PostgreSQL.")
        return

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
            print("No se encontró ningún plato disponible con ese código.")
        print("-" * 40)
    except Exception as e:
        print(f"Error al consultar: {e}")
    finally:
        cursor.close()


def consulta_todos_platos():
    """SELECT GENERAL: Lista todos los platos almacenados en la base de datos."""
    if not esta_conectado():
        print("\n[ERROR BD] No hay conexión activa a la base de datos PostgreSQL.")
        return

    print("\n" + "=" * 65)
    print("         LISTADO GENERAL DE PLATOS EN POSTGRESQL        ")
    print("=" * 65)
    cursor = conexion.cursor()
    try:
        ordensql = """
            SELECT p.codigo, p.nombre, p.precio, c.nombre
            FROM platos p
            JOIN categorias c ON p.id_categoria = c.id_categoria
            WHERE p.disponible = TRUE
            ORDER BY 
                CASE 
                    WHEN p.codigo ~ '^[0-9]+$' THEN p.codigo::integer 
                    ELSE 999999 
                END, p.codigo ASC
        """
        cursor.execute(ordensql)
        platos = cursor.fetchall()
        print(f"{'CÓD':<6}{'NOMBRE DEL PLATO':<30}{'CATEGORÍA':<14}{'PRECIO':>12}")
        print("-" * 65)
        for p_item in platos:
            precio_fmt = f"${int(p_item[2]):,}".replace(",", ".")
            print(f"{p_item[0]:<6}{p_item[1]:<30}{p_item[3]:<14}{precio_fmt:>12}")
        print("=" * 65)
    except Exception as e:
        print(f"Error al listar platos: {e}")
    finally:
        cursor.close()


def actualiza_plato():
    """UPDATE: Actualiza el precio o el nombre de un plato en la base de datos."""
    if not esta_conectado():
        print("\n[ERROR BD] No hay conexión activa a la base de datos PostgreSQL.")
        return

    print("\n" + "-" * 40)
    print("          ACTUALIZANDO PLATO           ")
    print("-" * 40)
    cod = input("Ingrese el código del plato a actualizar: ").strip()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT nombre FROM platos WHERE codigo = %s AND disponible = TRUE", (cod,))
        plato_existe = cursor.fetchone()
        if not plato_existe:
            print("-" * 40)
            print(f"El plato con código '{cod}' no existe o está retirado.")
            return

        print(f"Plato seleccionado: {plato_existe[0]}")
        campo = input("Ingrese el dato a actualizar (1-Nombre, 2-Precio): ").strip()
        if campo == "1":
            nuevo_nombre = input("Ingrese el nuevo nombre del plato: ").strip()
            if not nuevo_nombre:
                print("El nombre no puede estar vacío.")
                return
            ordensql = "UPDATE platos SET nombre = %s WHERE codigo = %s"
            cursor.execute(ordensql, (nuevo_nombre, cod))
        elif campo == "2":
            nuevo_precio = float(input("Ingrese el nuevo precio del plato: ").strip())
            if nuevo_precio <= 0:
                print("El precio debe ser mayor a 0.")
                return
            ordensql = "UPDATE platos SET precio = %s WHERE codigo = %s"
            cursor.execute(ordensql, (nuevo_precio, cod))
        else:
            print("Opción no válida.")
            return

        if cursor.rowcount > 0:
            conexion.commit()
            sincronizar_con_menu()
            print("-" * 40)
            print("¡Plato actualizado con éxito en la base de datos!")
        else:
            conexion.rollback()
            print("-" * 40)
            print(f"No se pudo actualizar el plato con código '{cod}'.")
    except Exception as e:
        conexion.rollback()
        print(f"Error al actualizar: {e}")
    finally:
        cursor.close()


def eliminar_plato():
    """DELETE lógico: Da de baja un plato en la base de datos cambiando su estado a disponible = FALSE."""
    if not esta_conectado():
        print("\n[ERROR BD] No hay conexión activa a la base de datos PostgreSQL.")
        return

    print("\n" + "-" * 40)
    print("           RETIRANDO PLATO             ")
    print("-" * 40)
    cod = input("Ingrese el código del plato a retirar/borrar: ").strip()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT nombre FROM platos WHERE codigo = %s AND disponible = TRUE", (cod,))
        plato_existe = cursor.fetchone()
        if not plato_existe:
            print("-" * 40)
            print(f"El plato con código '{cod}' no existe o ya está retirado.")
            return

        ordensql = "UPDATE platos SET disponible = FALSE WHERE codigo = %s AND disponible = TRUE"
        cursor.execute(ordensql, (cod,))
        if cursor.rowcount > 0:
            conexion.commit()
            sincronizar_con_menu()
            print("-" * 40)
            print(f"¡Plato '{plato_existe[0]}' (Cód: {cod}) retirado exitosamente de la carta!")
        else:
            conexion.rollback()
            print("-" * 40)
            print(f"No se encontró ningún plato activo con el código '{cod}'.")
    except Exception as e:
        conexion.rollback()
        print(f"Error al retirar plato: {e}")
    finally:
        cursor.close()


def obtener_catalogo_bd():
    """Consulta los platos disponibles en BD para alimentar menu.py (fuente de verdad única).
    Retorna un diccionario de platos (puede estar vacío {} si no hay platos disponibles), o None si hay error."""
    if not esta_conectado():
        return None

    cursor = conexion.cursor()
    try:
        ordensql = """
            SELECT p.codigo, p.nombre, p.precio, p.descripcion, c.nombre
            FROM platos p
            JOIN categorias c ON p.id_categoria = c.id_categoria
            WHERE p.disponible = TRUE
            ORDER BY 
                CASE 
                    WHEN p.codigo ~ '^[0-9]+$' THEN p.codigo::integer 
                    ELSE 999999 
                END, p.codigo ASC
        """
        cursor.execute(ordensql)
        filas = cursor.fetchall()
        catalogo = {}
        for fila in filas:
            catalogo[str(fila[0])] = {
                "nombre": fila[1],
                "precio": float(fila[2]),
                "descripcion": fila[3] or "",
                "categoria": fila[4]
            }
        return catalogo
    except Exception as e:
        print(f"[BD] Error al consultar catálogo de platos: {e}")
        return None
    finally:
        cursor.close()


def sincronizar_con_menu():
    """Sincroniza el catálogo de la BD con el diccionario en memoria de menu.py."""
    if not esta_conectado():
        return False
    try:
        import menu
        cat_bd = obtener_catalogo_bd()
        if cat_bd is not None:
            # cat_bd puede ser un diccionario con platos o {} si se retiraron todos
            menu.PLATOS.clear()
            menu.PLATOS.update(cat_bd)
            return True
        return False
    except Exception as e:
        print(f"[BD] Error al sincronizar con el menú: {e}")
        return False


def guardar_pedido_bd(cliente, orden, subtotal, impoconsumo, total):
    """Inserta el pedido y su detalle en PostgreSQL."""
    if not esta_conectado():
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
        print(f"\n[AVISO BD] No se pudo guardar el pedido en PostgreSQL: {e}")
        return None
    finally:
        cursor.close()


def terminar():
    """Cierra la conexión con la base de datos."""
    global conexion
    if esta_conectado():
        conexion.close()
        conexion = None
        print("Conexión con PostgreSQL cerrada.")
