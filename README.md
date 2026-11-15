# Gourmet Restaurant - Fase 3 (Proyecto ABP)

Sistema interactivo de gestión para restaurante desarrollado en Python con persistencia en **PostgreSQL** y compatibilidad multiplataforma (**Windows**, **Linux**, **macOS**).

## 👥 Integrantes
* Jesús Esteban Muñoz Gómez
* Albeiro Andrés Rodgers Pérez
* Alex Javier Campo Suárez

---

## 🏗️ Arquitectura y Estructura del Proyecto

* **`main.py`**: Punto de entrada del programa. Controla el menú interactivo, la navegación por categorías, flujo de pedidos, facturación y el submenú de administración.
* **`crud_restaurante.py`**: Módulo central de base de datos. Implementa las operaciones CRUD completas en PostgreSQL (`INSERT`, `SELECT`, `UPDATE`, `DELETE` lógico), actualización de la carta en memoria y fallback local si la BD no está disponible.
* **`menu.py`**: Catálogo de productos (`PLATOS`). Contiene la carta base predeterminada y se actualiza desde PostgreSQL cuando la base de datos está conectada.
* **`restaurant.py`**: Lógica de gestión de pedidos. Maneja el carrito (`orden_actual`), cálculo de subtotales, impoconsumo (8%), emisión de factura en archivo `.txt` y registro transaccional en la BD.
* **`titles.py`**: Formatos visuales, banners, encabezados ASCII y la función multiplataforma para limpiar pantalla.
* **`restaurante.sql`**: Script DDL y DML para la creación de las 4 tablas relacionales (`categorias`, `platos`, `pedidos`, `detalle_pedidos`) y la carga inicial de los 25 platos.

---

## ⚙️ Requisitos Previos e Instalación

### 1. Requisitos
* Python 3.10 o superior (Windows, Linux o macOS).
* PostgreSQL 12 o superior (opcional; si no está activo o instalado, el sistema arranca limpiamente en **Modo Local**).

### 2. Dependencias de Python
Instalar el conector de PostgreSQL para Python:
```bash
pip install psycopg2-binary
```
*(Nota: Si no se instala `psycopg2`, el sistema funcionará normalmente en **Modo Local** con la carta interna).*

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
El sistema detecta automáticamente al usuario del sistema (`$USER` en Linux/Mac y `%USERNAME%` en Windows) o el usuario estándar `postgres`. Si tu PostgreSQL requiere credenciales o puertos personalizados, configúralos antes de ejecutar:

* **En Linux / macOS:**
  ```bash
  export DB_NAME="restaurante_gourmet"
  export DB_USER="tu_usuario"
  export DB_PASSWORD="tu_password"
  export DB_HOST="localhost"
  export DB_PORT="5432"
  ```

* **En Windows (CMD):**
  ```cmd
  set DB_NAME=restaurante_gourmet
  set DB_USER=tu_usuario
  set DB_PASSWORD=tu_password
  set DB_HOST=localhost
  set DB_PORT=5432
  ```

* **En Windows (PowerShell):**
  ```powershell
  $env:DB_NAME="restaurante_gourmet"
  $env:DB_USER="tu_usuario"
  $env:DB_PASSWORD="tu_password"
  $env:DB_HOST="localhost"
  $env:DB_PORT="5432"
  ```

---

## 🚀 Cómo Ejecutar el Proyecto

1. Abrir la terminal en la carpeta del proyecto.
2. Ejecutar el comando:
   * **En Windows:**
     ```bash
     python main.py
     ```
   * **En Linux / macOS:**
     ```bash
     python3 main.py
     ```

---

## 📋 Funcionalidades Principales

1. **Tolerancia a fallos:** Si PostgreSQL está apagado o no instalado, el sistema arranca limpiamente en **Modo Local** indicando en pantalla el motivo exacto (ej. falta de librería o base de datos no iniciada) sin romperse jamás.
2. **Fuente de verdad única:** Si la base de datos está conectada, el menú de pedidos se actualiza desde PostgreSQL. Si registras, modificas o retiras un plato en la Opción 7 (Admin), la carta se actualiza de inmediato para los pedidos.
3. **Manejo de categorías vacías:** Si una categoría no tiene platos disponibles, el sistema informa amablemente al usuario sin pedir códigos inexistentes.
4. **Panel de Administración (CRUD Completo):**
   * **`INSERT`**: Registrar nuevos platos con validación de categorías y precio (o reactivar platos retirados).
   * **`SELECT`**: Consulta individual por código y listado tabular ordenado de la carta.
   * **`UPDATE`**: Modificación de nombres y precios.
   * **`DELETE`**: Retiro lógico (`disponible = FALSE`) protegiendo el histórico de pedidos.
5. **Facturación y Transacciones:**
   * Cálculo automático de subtotales, 8% de impoconsumo y total.
   * Exportación de recibo en `factura_venta.txt`.
   * Registro atómico en PostgreSQL en las tablas `pedidos` y `detalle_pedidos` con rollback automático si algo falla.
