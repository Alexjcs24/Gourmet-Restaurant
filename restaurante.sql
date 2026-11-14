-- =====================================================================
-- PROYECTO INTEGRADOR ABP - FASE 3
-- ASIGNATURA: PROGRAMACIÓN I
-- INTEGRANTES:
--   - Jesús Esteban Muñoz Gómez
--   - Albeiro Andrés Rodgers Pérez
--   - Alex Javier Campo Suárez
-- ARCHIVO: restaurante.sql
-- DESCRIPCIÓN: Creación de la base de datos, tablas, restricciones
--              e inserción de los 25 platos iniciales de la carta.
-- =====================================================================

-- 1. CREACIÓN DE LA BASE DE DATOS (Ejecutar en PostgreSQL / pgAdmin si no existe)
-- CREATE DATABASE restaurante_gourmet;
-- \c restaurante_gourmet;

-- Eliminar tablas si ya existen para permitir reinicios limpios
DROP TABLE IF EXISTS detalle_pedidos CASCADE;
DROP TABLE IF EXISTS pedidos CASCADE;
DROP TABLE IF EXISTS platos CASCADE;
DROP TABLE IF EXISTS categorias CASCADE;

-- =====================================================================
-- TABLA 1: Categorías del Menú
-- =====================================================================
CREATE TABLE categorias (
    id_categoria SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

-- =====================================================================
-- TABLA 2: Platos de la Carta
-- =====================================================================
CREATE TABLE platos (
    codigo VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio NUMERIC(10, 2) NOT NULL CHECK (precio > 0),
    descripcion TEXT,
    id_categoria INT NOT NULL,
    disponible BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_plato_categoria FOREIGN KEY (id_categoria) 
        REFERENCES categorias(id_categoria) ON DELETE RESTRICT
);

-- =====================================================================
-- TABLA 3: Pedidos / Facturas Registradas
-- =====================================================================
CREATE TABLE pedidos (
    id_pedido SERIAL PRIMARY KEY,
    cliente VARCHAR(100) NOT NULL DEFAULT 'Consumidor Final',
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    subtotal NUMERIC(10, 2) NOT NULL CHECK (subtotal >= 0),
    impoconsumo NUMERIC(10, 2) NOT NULL CHECK (impoconsumo >= 0),
    total NUMERIC(10, 2) NOT NULL CHECK (total >= 0),
    estado VARCHAR(20) DEFAULT 'PAGADO' CHECK (estado IN ('PENDIENTE', 'PAGADO', 'CANCELADO'))
);

-- =====================================================================
-- TABLA 4: Detalle de cada Pedido
-- =====================================================================
CREATE TABLE detalle_pedidos (
    id_detalle SERIAL PRIMARY KEY,
    id_pedido INT NOT NULL,
    codigo_plato VARCHAR(10) NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(10, 2) NOT NULL,
    subtotal_linea NUMERIC(10, 2) NOT NULL,
    CONSTRAINT fk_detalle_pedido FOREIGN KEY (id_pedido) 
        REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    CONSTRAINT fk_detalle_plato FOREIGN KEY (codigo_plato) 
        REFERENCES platos(codigo) ON DELETE RESTRICT
);

-- =====================================================================
-- INSERCIÓN DE DATOS INICIALES (CATEGORÍAS)
-- =====================================================================
INSERT INTO categorias (id_categoria, nombre) VALUES
(1, 'Desayuno'),
(2, 'Almuerzo'),
(3, 'Postre');

-- Ajustar la secuencia de categorías
SELECT setval('categorias_id_categoria_seq', 3, true);

-- =====================================================================
-- INSERCIÓN DE LOS 25 PLATOS DE LA CARTA
-- =====================================================================

-- --- DESAYUNOS (id_categoria = 1) ---
INSERT INTO platos (codigo, nombre, precio, descripcion, id_categoria) VALUES
('1', 'Croissant Pistacho', 12000, 'Croissant hojaldrado relleno de crema de pistacho artesanal.', 1),
('2', 'Huevos Puntilla', 9500, 'Huevos fritos con borde crujiente al estilo tradicional campesino.', 1),
('3', 'Tostada Parisina', 11000, 'Pan brioche dorado con mantequilla, queso gruyère y jamón.', 1),
('4', 'Croissant Lemon', 10500, 'Croissant relleno de suave crema de limón y glaseado.', 1),
('5', 'Pan de Nuez', 6500, 'Pan artesanal horneado con nueces seleccionadas.', 1),
('6', 'Arepa de Huevo', 6000, 'Típica arepa costeña de maíz amarillo rellena con huevo frito.', 1),
('7', 'Empanada de Carne', 4500, 'Empanada crujiente rellena de carne desmechada sazonada.', 1),
('8', 'Empanada de Pollo', 4500, 'Empanada crocante rellena de pechuga de pollo y guiso casero.', 1),
('9', 'Empanada Hawaiana', 4500, 'Empanada rellena de jamón, queso derretido y piña calada.', 1);

-- --- ALMUERZOS (id_categoria = 2) ---
INSERT INTO platos (codigo, nombre, precio, descripcion, id_categoria) VALUES
('10', 'Chicken Parm', 28000, 'Pechuga empanizada con salsa marinara casera y queso mozzarella gratinado.', 2),
('11', 'Pollo Toscano', 29500, 'Pechuga en salsa cremosa de tomates secos, espinacas y ajo.', 2),
('12', 'Pollo a la Cacerola', 26000, 'Guiso tradicional de pollo cocinado a fuego lento con vegetales y papas.', 2),
('13', 'Paella Mixta', 35000, 'Arroz español con mariscos variados, pollo, cerdo y azafrán.', 2),
('14', 'Salmón Pataraska', 38000, 'Filete de salmón fresco envuelto en hoja de plátano con especias autóctonas.', 2);

-- --- POSTRES (id_categoria = 3) ---
INSERT INTO platos (codigo, nombre, precio, descripcion, id_categoria) VALUES
('15', 'Tiramisú', 16900, 'Postre italiano con capas de bizcocho al café, crema de queso y cacao.', 3),
('16', 'Volcán de Arequipe', 17900, 'Bizcocho tibio con centro fundido de arequipe, fresas y helado de vainilla.', 3),
('17', 'Volcán de Chocolate', 17900, 'Bizcocho con centro líquido de chocolate oscuro, fresas y helado de vainilla.', 3),
('18', 'Stromboli de Chocolate', 17900, 'Capas de bizcocho suave con ganache de chocolate intenso y café.', 3),
('19', 'Gelato Cheese de Limón', 7500, 'Helado cremoso de tarta de queso con notas de limón y crumble de galleta.', 3),
('20', 'Gelato Chocolate Dubai', 17900, 'Gelato de chocolate fino, crema de pistacho tostado y crujiente de hojaldre.', 3),
('21', 'Gelato Pistaccio', 7500, 'Helado artesanal elaborado con auténtico pistacho natural tostado.', 3),
('22', 'Tarta Vasca', 15000, 'Clásica cheesecake horneada al estilo San Sebastián, tostada y cremosa.', 3),
('23', 'Baklava', 13500, 'Dulce turco de masa filo relleno de nueces picadas y bañado en miel.', 3),
('24', 'Torta de Almojábana', 11000, 'Postre tradicional a base de maíz y cuajada con toque de caramelo.', 3),
('25', 'Helado Napolitano', 6500, 'Combinación clásica de tres sabores: fresa, vainilla y chocolate.', 3);
