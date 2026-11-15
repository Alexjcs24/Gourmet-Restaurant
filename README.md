# Gourmet Restaurant - Fase 3 (Proyecto ABP)

Sistema interactivo de gestión para restaurante desarrollado en Python con persistencia en **PostgreSQL**.

## 👥 Integrantes
* Jesús Esteban Muñoz Gómez
* Albeiro Andrés Rodgers Pérez
* Alex Javier Campo Suárez

---

## 🏗️ Arquitectura y Estructura del Proyecto

* **`main.py`**: Punto de entrada del programa. Controla el menú interactivo, la navegación por categorías, flujo de facturación y el submenú de administración.
* **`crud_restaurante.py`**: Módulo central de base de datos. Implementa las operaciones CRUD completas en PostgreSQL (`INSERT`, `SELECT`, `UPDATE`, `DELETE` lógico), sincronización bidireccional y fallback local si la BD no está disponible.
* **`menu.py`**: Catálogo de productos (`PLATOS`). Sirve como respaldo local cuando no hay base de datos y se sincroniza en tiempo real con PostgreSQL cuando la BD está conectada.
* **`restaurant.py`**: Lógica de gestión de pedidos. Maneja el carrito (`orden_actual`), cálculo de subtotales, impoconsumo (8%), emisión de factura en archivo `.txt` y registro transaccional en la BD.
* **`titles.py`**: Formatos visuales, banners, encabezados ASCII y la función multiplataforma para limpiar pantalla.
* **`database.py`**: Módulo fachada que garantiza retrocompatibilidad con las funciones del docente.
* **`restaurante.sql`**: Script DDL y DML para la creación de las 4 tablas relacionales (`categorias`, `platos`, `pedidos`, `detalle_pedidos`) y la carga inicial de los 25 platos.

---

## ⚙️ Requisitos Previos e Instalación

### 1. Requisitos
* Python 3.10 o superior.
* PostgreSQL 12 o superior (opcional pero recomendado para persistencia y panel CRUD).

### 2. Dependencias de Python
Instalar el conector de PostgreSQL para Python:
```bash
pip install psycopg2-binary
```
*(Nota: Si no se instala `psycopg2`, el sistema funcionará normalmente en **Modo Local**).*

---

## 🗄️ Configuración de la Base de Datos (PostgreSQL)

### Paso 1: Crear la Base de Datos
Desde la terminal o consola `psql`:
```bash
createdb restaurante_gourmet
```
O dentro de `psql` / pgAdmin:
```sql
CREATE DATABASE restaurante_gourmet;
```

### Paso 2: Ejecutar el script SQL
Cargue las tablas y los datos iniciales con:
```bash
psql -d restaurante_gourmet -f restaurante.sql
```
*(O copie y pegue el contenido de `restaurante.sql` en la herramienta Query Tool de pgAdmin).*

### Paso 3: Variables de Conexión (Opcional)
Por defecto el sistema intentará conectarse usando tu usuario del sistema o el usuario estándar `postgres`. Si tu PostgreSQL requiere credenciales específicas, puedes configurarlas en la terminal antes de iniciar:
```bash
export DB_NAME="restaurante_gourmet"
export DB_USER="tu_usuario_postgres"
export DB_PASSWORD="tu_password"
export DB_HOST="localhost"
export DB_PORT="5432"
```

---

## 🚀 Cómo Ejecutar el Proyecto

1. Abrir la terminal en la carpeta del proyecto.
2. Ejecutar el comando:
   ```bash
   python main.py
   ```
   *(En Linux / Mac: `python3 main.py`)*

---

## 📋 Funcionalidades Principales

1. **Tolerancia a fallos:** Si PostgreSQL está apagado o no instalado, el sistema arranca limpiamente en **Modo Local** sin romperse.
2. **Fuente de verdad única:** Si la base de datos está conectada, el menú de pedidos lee directamente los platos disponibles de PostgreSQL. Si registras o retiras un plato en la Opción 7 (Admin), la carta se actualiza de inmediato.
3. **Panel de Administración (CRUD Completo):**
   * **`INSERT`**: Registrar nuevos platos con validación de categorías y precio.
   * **`SELECT`**: Consulta individual por código y listado tabular ordenado de la carta.
   * **`UPDATE`**: Modificación de nombres y precios.
   * **`DELETE`**: Retiro lógico (`disponible = FALSE`) protegiendo el histórico de pedidos.
4. **Facturación y Transacciones:**
   * Cálculo automático de subtotales, 8% de impoconsumo y total.
   * Exportación de recibo en `factura_venta.txt`.
   * Registro atómico en PostgreSQL en las tablas `pedidos` y `detalle_pedidos` con rollback automático si algo falla.
