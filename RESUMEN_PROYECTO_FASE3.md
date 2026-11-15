# 📘 Resumen Ejecutivo y Guía de Sustentación - Fase 3
**Proyecto Integrador ABP: Restaurante Gourmet**  
**Integrantes:** Jesús Esteban Muñoz Gómez, Albeiro Andrés Rodgers Pérez, Alex Javier Campo Suárez  
**Repositorio GitHub:** [https://github.com/Alexjcs24/Gourmet-Restaurant](https://github.com/Alexjcs24/Gourmet-Restaurant)

---

## 1. Estado Actual del Proyecto
El proyecto cumple con los requerimientos de la Fase 3:
- **Modularización:** Dividido en `main.py`, `menu.py`, `restaurant.py`, `titles.py`, `crud_restaurante.py` y `database.py`.
- **Base de Datos Relacional:** `restaurante.sql` implementado en PostgreSQL con 4 tablas (`categorias`, `platos`, `pedidos`, `detalle_pedidos`) y restricciones de integridad.
- **Operaciones CRUD Completas:**
  - `INSERT`: Registro de pedidos/facturas y alta de nuevos platos.
  - `SELECT`: Consulta individual por código y listado general de la carta.
  - `UPDATE`: Actualización de nombres y precios de platos.
  - `DELETE`: Retiro de platos de la carta.
- **Herramienta visual:** Conectado y verificado en **pgAdmin 4** con el usuario `alexcs`.

---

## 2. Comandos Clave para Ejecutar y Probar

### En la terminal (VS Code):
```bash
# Iniciar el sistema
python3 main.py

# Ingresar a la consola interactiva de PostgreSQL directamente
psql -d restaurante_gourmet -U alexcs
```

### Consultas útiles en PostgreSQL / pgAdmin:
```sql
-- Ver todos los platos
SELECT * FROM platos;

-- Ver los pedidos realizados
SELECT * FROM pedidos;

-- Ver el detalle de los productos en cada factura
SELECT * FROM detalle_pedidos;
```

---

## 3. Conceptos Clave para la Sustentación Oral y Metodológica
Para la sustentación oral del proyecto integrador, es indispensable dominar estos conceptos técnicos fundamentales:
1. **`psycopg2`**: Librería controladora que permite a Python comunicarse con el motor de PostgreSQL.
2. **`cursor`**: Objeto puente que envía comandos SQL y recupera los registros consultados (`fetchone`, `fetchall`).
3. **`commit()`**: Método obligatorio que confirma y consolida las transacciones (`INSERT`, `UPDATE`, `DELETE`) en el disco duro.
4. **`rollback()`**: Se usa dentro del bloque `except` para revertir la operación si ocurre un error y no dejar la base de datos corrupta.
5. **Parámetros `%s`**: Uso de tuplas de argumentos para prevenir inyecciones SQL y formatear datos de manera segura.

---

## 4. Pendientes para la Próxima Sesión
- [ ] Implementar la versión en inglés (carpeta `en/`) para la demostración en video.
- [ ] Diseñar la tabla de los 8 Casos de Prueba (Producto 5 de la guía).
- [ ] Redactar las secciones correspondientes del documento metodológico final.
