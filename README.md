# 🍽️ Gourmet Restaurant

Sistema modular en consola para la toma de pedidos y facturación de un restaurante.

---

## 👥 Integrantes del Proyecto

- **Jesús Esteban Muñoz Gómez**
- **Albeiro Andrés Rodgers Pérez**
- **Alex Javier Campo Suárez**

---

## 📁 Estructura del Código

El proyecto está dividido en 4 módulos en Python:

| Archivo | Responsabilidad |
| :--- | :--- |
| **[`main.py`](main.py)** | Punto de entrada del programa. Controla el menú interactivo, la selección de opciones y la navegación entre categorías. |
| **[`menu.py`](menu.py)** | Catálogo de platos (`PLATOS`) organizados por Desayunos, Almuerzos y Postres, junto con las funciones para listarlos en consola. |
| **[`restaurant.py`](restaurant.py)** | Gestión de la orden activa (agregar productos, calcular subtotal, impoconsumo del 8% y total), cancelación de orden y exportación de la factura a archivo `.txt`. |
| **[`titles.py`](titles.py)** | Encabezados de texto formateados para cada sección y función para limpiar la consola. |

---

## 🚀 Requisitos y Ejecución

### Requisitos
- **Python 3.10 o superior** (el proyecto utiliza la sentencia de coincidencia de patrones `match / case` introducida en Python 3.10).

### Cómo ejecutar el programa
```bash
python3 main.py
```
*(En Windows ejecutar con `python main.py`)*

---

## ⚙️ Funcionamiento y Reglas de Negocio

- **Categorías disponibles:** Desayunos, Almuerzos y Postres.
- **Impuestos aplicados:** Impuesto Nacional al Consumo (**Impoconsumo del 8%**) sobre el subtotal acumulado.
- **Facturación:** Al confirmar el pedido, además de mostrar el detalle en pantalla, se genera un archivo de texto con el comprobante de la compra (`factura_<cliente>.txt`).
