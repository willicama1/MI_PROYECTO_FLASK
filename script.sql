-- Crear la base de datos
CREATE DATABASE desarrollo_web;

-- Usar la base de datos
USE desarrollo_web;

-- Crear tabla de usuarios
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    correo VARCHAR(100)
);
