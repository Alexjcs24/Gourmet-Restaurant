# 🍽️ Gourmet Restaurant

Sistema modular de pedidos, gestión de comandas y facturación interactiva para un restaurante por consola en Python.

---

## 👥 Integrantes del Proyecto

- **Jesús Esteban Muñoz Gómez**
- **Albeiro Andrés Rodgers Pérez**
- **Alex Javier Campo Suárez**

---

## 📁 Estructura del Proyecto

El código está organizado de forma modular para que sea fácil de mantener y extender:

| Archivo | Descripción |
| :--- | :--- |
| **[`main.py`](main.py)** | **Punto de entrada principal**. Maneja el flujo de la aplicación, interacción con el usuario, selección de categorías y navegación del menú. |
| **[`menu.py`](menu.py)** | **Catálogo de platos y bebidas**. Contiene el diccionario centralizado `PLATOS` con códigos, nombres, precios y categorías, además de las funciones para visualizarlos en pantalla. |
| **[`restaurant.py`](restaurant.py)** | **Lógica del pedido y facturación**. Administra la lista de pedidos activos, cálculo de subtotales, IVA (19%), propina voluntaria (10%) y generación del comprobante fiscal. |
| **[`titles.py`](titles.py)** | **Diseño visual e interfaces**. Banners ASCII, encabezados formateados y utilidades de consola (como limpieza de pantalla). |

---

## 🚀 Requisitos y Ejecución

### Requisitos
- **Python 3.8** o superior (no requiere librerías externas adicionales).

### Cómo ejecutar el proyecto
1. Clona el repositorio (si aún no lo tienes):
   ```bash
   git clone https://github.com/Alexjcs24/Gourmet-Restaurant.git
   cd Gourmet-Restaurant
   ```

2. Ejecuta el archivo principal:
   ```bash
   python3 main.py
   ```
   *(En Windows puedes usar `python main.py`)*

---

## 💡 Guía para Colaboradores

Si vas a agregar o editar contenido:
- **Agregar nuevos platos o cambiar precios:** Edita únicamente el diccionario `PLATOS` dentro de [`menu.py`](menu.py).
- **Modificar cálculos o la factura:** Revisa [`restaurant.py`](restaurant.py).
- **Personalizar textos o banners:** Edita [`titles.py`](titles.py).
- **Nuevas opciones de menú:** Conéctalas en el bucle interactivo de [`main.py`](main.py).
