# Gourmet Restaurant - Fase 3

Proyecto universitario de gestión para restaurante desarrollado en Python.

## Integrantes
* Jesús Esteban Muñoz Gómez
* Albeiro Andrés Rodgers Pérez
* Alex Javier Campo Suárez

---

## Estructura del Proyecto

* **`main.py`**: Punto de entrada del programa. Controla el menú interactivo, la navegación por categorías y el flujo de facturación.
* **`menu.py`**: Catálogo general de productos (`PLATOS`). Contiene los desayunos, almuerzos y postres organizados con códigos, precios y descripciones.
* **`restaurant.py`**: Lógica de gestión de pedidos. Maneja el carrito (`orden_actual`), cálculo de subtotales, impoconsumo (8%) y generación de factura.
* **`titles.py`**: Formatos visuales, banners, encabezados y la función para limpiar pantalla en cualquier sistema operativo.

---

## Cómo ejecutar el proyecto en VS Code

1. Abrir la carpeta del proyecto en Visual Studio Code.
2. Abrir la terminal integrada (`Ctrl + Ñ` o `Terminal -> New Terminal`).
3. Ejecutar el comando:
   ```bash
   python main.py
   ```
   *(En Linux / Mac: `python3 main.py`)*

---

## Funcionalidades
1. **Navegación por categorías:** Selección clara de Desayunos, Almuerzos y Postres.
2. **Carrito interactivo:** Permite agregar múltiples platos indicando cantidades sin romper la ejecución.
3. **Cálculo automático:** Subtotales, 8% de impoconsumo y total a pagar.
4. **Emisión de factura:** Imprime la factura en pantalla y guarda automáticamente un respaldo en `factura_venta.txt`.
