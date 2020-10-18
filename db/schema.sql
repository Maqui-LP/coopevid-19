-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Servidor: db
-- Tiempo de generación: 18-10-2020 a las 01:13:49
-- Versión del servidor: 10.5.6-MariaDB-1:10.5.6+maria~focal
-- Versión de PHP: 7.4.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `proyecto`
--
CREATE DATABASE IF NOT EXISTS `proyecto` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `proyecto`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categories`
--

DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `categories`
--

INSERT INTO `categories` (`id`, `name`) VALUES
(1, 'Bug'),
(2, 'Question');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `configuracion`
--

DROP TABLE IF EXISTS `configuracion`;
CREATE TABLE `configuracion` (
  `id` int(11) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `mantenimiento` tinyint(1) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `contacto` varchar(255) NOT NULL,
  `paginacion` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `configuracion`
--

INSERT INTO `configuracion` (`id`, `titulo`, `mantenimiento`, `descripcion`, `contacto`, `paginacion`) VALUES
(1, 'Donaciones COVID-19', 0, 'Esta pagina esta destinada a colaborar en la lucha contra el COVID-19', 'contacto@coopevid.com', 5);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `issues`
--

DROP TABLE IF EXISTS `issues`;
CREATE TABLE `issues` (
  `id` int(11) NOT NULL,
  `email` varchar(30) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `category_id` int(10) NOT NULL,
  `status_id` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `issues`
--

INSERT INTO `issues` (`id`, `email`, `description`, `category_id`, `status_id`) VALUES
(1, 'fede@mail.com', 'No puedo iniciar sesión correctamente', 1, 1),
(2, 'jose@mail.com', 'El sistema de dice que hay un error', 1, 2),
(4, 'maria@mail.com', 'No tengo acceso al sistema', 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permiso`
--

DROP TABLE IF EXISTS `permiso`;
CREATE TABLE `permiso` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `permiso`
--

INSERT INTO `permiso` (`id`, `nombre`) VALUES
(13, 'categoria_destroy'),
(11, 'categoria_index'),
(12, 'categoria_new'),
(15, 'categoria_show'),
(14, 'categoria_update'),
(21, 'configuracion_update'),
(18, 'issue_destroy'),
(16, 'issue_index'),
(17, 'issue_new'),
(20, 'issue_show'),
(19, 'issue_update'),
(8, 'rol_destroy'),
(6, 'rol_index'),
(7, 'rol_new'),
(10, 'rol_show'),
(9, 'rol_update'),
(3, 'usuario_destroy'),
(1, 'usuario_index'),
(2, 'usuario_new'),
(5, 'usuario_show'),
(4, 'usuario_update');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol`
--

DROP TABLE IF EXISTS `rol`;
CREATE TABLE `rol` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `rol`
--

INSERT INTO `rol` (`id`, `nombre`) VALUES
(1, 'Administrador'),
(2, 'Operador');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol_tiene_permiso`
--

DROP TABLE IF EXISTS `rol_tiene_permiso`;
CREATE TABLE `rol_tiene_permiso` (
  `rol_id` int(11) NOT NULL,
  `permiso_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `rol_tiene_permiso`
--

INSERT INTO `rol_tiene_permiso` (`rol_id`, `permiso_id`) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(1, 6),
(1, 7),
(1, 8),
(1, 9),
(1, 10),
(1, 11),
(1, 12),
(1, 13),
(1, 14),
(1, 15),
(1, 16),
(1, 17),
(1, 18),
(1, 19),
(1, 20),
(1, 21);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `statuses`
--

DROP TABLE IF EXISTS `statuses`;
CREATE TABLE `statuses` (
  `id` int(11) NOT NULL,
  `name` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `statuses`
--

INSERT INTO `statuses` (`id`, `name`) VALUES
(1, 'New'),
(2, 'Todo'),
(3, 'In progress');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `updated_at` datetime DEFAULT NULL,
  `created_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `first_name`, `last_name`, `activo`, `updated_at`, `created_at`) VALUES
(1, 'admin', 'admin@coopevid.com', 'sha256$q7bSSMwZ$d125a6aeaf2172af3874b8dbfe64e8eed969d02e5c7f50c5f4c91a9e723c46e5', 'Admin', 'Fulanito', 1, '0000-00-00 00:00:00', '0000-00-00 00:00:00'),
(2, 'operador', 'operador@coopevid.com', 'sha256$q7bSSMwZ$d125a6aeaf2172af3874b8dbfe64e8eed969d02e5c7f50c5f4c91a9e723c46e5', 'Operador', 'Fulanito', 1, '0000-00-00 00:00:00', '0000-00-00 00:00:00'),
(3, 'nadie', 'nadie@coopevid.com', 'sha256$q7bSSMwZ$d125a6aeaf2172af3874b8dbfe64e8eed969d02e5c7f50c5f4c91a9e723c46e5', 'Cosme', 'Fulanito', 1, '0000-00-00 00:00:00', '0000-00-00 00:00:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_tiene_rol`
--

DROP TABLE IF EXISTS `usuario_tiene_rol`;
CREATE TABLE `usuario_tiene_rol` (
  `usuario_id` int(11) NOT NULL,
  `rol_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `usuario_tiene_rol`
--

INSERT INTO `usuario_tiene_rol` (`usuario_id`, `rol_id`) VALUES
(1, 1),
(2, 2);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `configuracion`
--
ALTER TABLE `configuracion`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `issues`
--
ALTER TABLE `issues`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`),
  ADD KEY `status_id` (`status_id`);

--
-- Indices de la tabla `permiso`
--
ALTER TABLE `permiso`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `rol_tiene_permiso`
--
ALTER TABLE `rol_tiene_permiso`
  ADD PRIMARY KEY (`rol_id`,`permiso_id`),
  ADD KEY `permiso_id` (`permiso_id`);

--
-- Indices de la tabla `statuses`
--
ALTER TABLE `statuses`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `usuario_tiene_rol`
--
ALTER TABLE `usuario_tiene_rol`
  ADD PRIMARY KEY (`usuario_id`,`rol_id`),
  ADD KEY `rol_id` (`rol_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `configuracion`
--
ALTER TABLE `configuracion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `issues`
--
ALTER TABLE `issues`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `permiso`
--
ALTER TABLE `permiso`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `rol`
--
ALTER TABLE `rol`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `statuses`
--
ALTER TABLE `statuses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `issues`
--
ALTER TABLE `issues`
  ADD CONSTRAINT `issues_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`),
  ADD CONSTRAINT `issues_ibfk_2` FOREIGN KEY (`status_id`) REFERENCES `statuses` (`id`);

--
-- Filtros para la tabla `rol_tiene_permiso`
--
ALTER TABLE `rol_tiene_permiso`
  ADD CONSTRAINT `rol_tiene_permiso_ibfk_1` FOREIGN KEY (`permiso_id`) REFERENCES `permiso` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `rol_tiene_permiso_ibfk_2` FOREIGN KEY (`rol_id`) REFERENCES `rol` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `usuario_tiene_rol`
--
ALTER TABLE `usuario_tiene_rol`
  ADD CONSTRAINT `usuario_tiene_rol_ibfk_1` FOREIGN KEY (`rol_id`) REFERENCES `rol` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `usuario_tiene_rol_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
