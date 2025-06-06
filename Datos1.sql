USE img;

-- PERFIL
INSERT INTO img.perfil (idPerfil, nombre_perfil) VALUES
(1, 'Chambrana'), (2, 'Riel'), (3, 'Cerco'), (4, 'Traslape'), (5, 'Zoclo'),
(6, 'Bolsa'), (7, 'Bolsa lisa'), (8, 'Escalonado'), (9, 'Riel adaptador'),
(10, 'Batiente 3/4"'), (11, 'Tapa bolsa'), (12, 'Tapa lisa'), (13, 'Intermedio'),
(14, 'Junquillo'), (15, 'Hamba'), (16, 'Riel doble'), (17, 'Riel triple');

-- SERIE
INSERT INTO img.serie (idSerie, nombre_serie) VALUES
(1, '2"'), (2, '3"'), (3, 'Pesada'), (4, '70');

-- COLOR
INSERT INTO img.color (idColor, nombre_color) VALUES
(1, 'Blanco'), (2, 'Negro'), (3, 'Natural'), (4, 'Champagne'),
(5, 'Madera Nogal'), (6, 'Madera Cerezo'), (7, 'Claro'), (8, 'Filtrasol'),
(9, 'Filtrasol plus'), (10, 'Tintex'), (11, 'Tintex plus'),
(12, 'Plata'), (13, 'Azul'), (14, 'Bronce');

-- TIPO CRISTAL
INSERT INTO img.tipo_cristal (idTipo_cristal, nombre_tipo) VALUES
(1, 'Normal'), (2, 'Templado'), (3, 'Inastillable'),
(4, 'Reflecta'), (5, 'Sol Lite');

-- ESPESOR
INSERT INTO img.espesor (idEspesor, medida_mm) VALUES
(1, '3 milimetros'), (2, '5 milimetros'), (3, '6 milimetros'),
(4, '10 milimetros'), (5, '12 milimetros'), (6, '19 milimetros');

-- CHAPA
INSERT INTO img.chapa (idChapa, tipo_chapa) VALUES
(1, 'Ninguno'), (2, 'Ciega'), (3, '545'), (4, '550'),
(5, 'Paleta'), (6, 'Tetra Gancho'), (7, 'Tetra Paleta'), (8, 'Guadalajara');

-- BISAGRAS
INSERT INTO img.bisagras (idBisagras, tipo_bisagra) VALUES
(1, 'Ninguno'), (2, 'Para serie 35'), (3, 'De libro'),
(4, 'Para serie 50'), (5, 'Pivote descentrado'), (6, 'Hidráulica');

-- JALADERAS
INSERT INTO img.jaladeras (idJaladeras, tipo_jaladeras) VALUES
(1, 'Ninguno'), (2, 'Trompa de elefante'), (3, 'Contra Plana'),
(4, 'Perico'), (5, 'Embutir para 2"'), (6, 'Embutir para 3"'),
(7, 'Tirador'), (8, 'Jaladera tipo H 45cm'), (9, 'Jaladera tipo H 90cm'),
(10, 'Jaladera tipo H 120cm'), (11, 'Jaladera tipo H 150cm');

-- CARRETAS
INSERT INTO img.carretas (idCarretas, nombre_carretas) VALUES
(1, 'Ninguno'), (2, 'Para mosquitero'), (3, 'Gorra de napoleón'),
(4, 'Para 3"'), (5, 'Para 3" reforzada'), (6, 'Para S70'),
(7, 'Para S80'), (8, 'Para S150');
