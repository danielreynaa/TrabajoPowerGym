-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS PowerGym;
USE PowerGym;

-- 1. Tabla Usuarios (Atletas, Entrenadores y Administradores)
CREATE TABLE IF NOT EXISTS Usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL, -- Guardar hash
    rol ENUM('Administrador', 'Entrenador', 'Atleta') NOT NULL, -- Ahora con 3 roles
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_nacimiento DATE,
    telefono VARCHAR(20),
    peso_corporal DECIMAL(5,2) -- Peso del atleta en kg (NULL para entrenadores/administradores)
);

-- 2. Tabla Entrenamientos (Sesiones de un atleta)
CREATE TABLE IF NOT EXISTS Entrenamientos (
    id_entrenamiento INT AUTO_INCREMENT PRIMARY KEY,
    id_atleta INT NOT NULL,
    fecha_entrenamiento DATE NOT NULL,
    notas TEXT,
    FOREIGN KEY (id_atleta) REFERENCES Usuarios(id_usuario)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- 3. Tabla RegistrosLevantamientos (Los 3 levantamientos principales)
CREATE TABLE IF NOT EXISTS RegistrosLevantamientos (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    id_entrenamiento INT NOT NULL,
    tipo_levantamiento ENUM('Sentadilla', 'Banca', 'Peso Muerto') NOT NULL,
    peso_kg DECIMAL(6,2) NOT NULL,
    repeticiones INT NOT NULL,
    series INT NOT NULL,
    rpe DECIMAL(3,1),
    FOREIGN KEY (id_entrenamiento) REFERENCES Entrenamientos(id_entrenamiento)
        ON DELETE CASCADE ON UPDATE CASCADE
);






