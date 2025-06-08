-- ---------------------------------------------------
-- 1. Crear Base de Datos y Tablas Principales
-- ---------------------------------------------------
CREATE DATABASE IF NOT EXISTS PowerGym;
USE PowerGym;

-- Tabla Usuarios
CREATE TABLE IF NOT EXISTS Usuarios (
    id_usuario       INT AUTO_INCREMENT PRIMARY KEY,
    nombre           VARCHAR(100) NOT NULL,
    apellidos        VARCHAR(100) NOT NULL,
    email            VARCHAR(100) NOT NULL UNIQUE,
    contrasena       VARCHAR(255) NOT NULL,          -- hash
    rol              ENUM('Administrador','Entrenador','Atleta') NOT NULL,
    fecha_registro   DATETIME      DEFAULT CURRENT_TIMESTAMP,
    fecha_nacimiento DATE,
    telefono         VARCHAR(20),
    peso_corporal    DECIMAL(5,2)                        -- kg, NULL para no-atletas
);

-- Tabla Entrenamientos
CREATE TABLE IF NOT EXISTS Entrenamientos (
    id_entrenamiento    INT AUTO_INCREMENT PRIMARY KEY,
    id_atleta           INT NOT NULL,
    fecha_entrenamiento DATE    NOT NULL,
    notas               TEXT,
    FOREIGN KEY (id_atleta)
        REFERENCES Usuarios(id_usuario)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Tabla RegistrosLevantamientos (sin id_usuario inicialmente)
CREATE TABLE IF NOT EXISTS RegistrosLevantamientos (
    id_registro         INT AUTO_INCREMENT PRIMARY KEY,
    id_entrenamiento    INT NOT NULL,
    tipo_levantamiento  ENUM('Sentadilla','Banca','Peso Muerto') NOT NULL,
    peso_kg             DECIMAL(6,2) NOT NULL,
    repeticiones        INT         NOT NULL,
    series              INT         NOT NULL,
    rpe                 DECIMAL(3,1),
    FOREIGN KEY (id_entrenamiento)
        REFERENCES Entrenamientos(id_entrenamiento)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- ---------------------------------------------------
-- 2. Añadir columna id_usuario (NULLABLE para poblar datos)
-- ---------------------------------------------------
ALTER TABLE RegistrosLevantamientos
  ADD COLUMN id_usuario INT NULL AFTER id_entrenamiento;


-- ---------------------------------------------------
-- 3. Rellenar id_usuario para los registros existentes
-- ---------------------------------------------------
UPDATE RegistrosLevantamientos RL
JOIN Entrenamientos E
  ON RL.id_entrenamiento = E.id_entrenamiento
SET RL.id_usuario = E.id_atleta;


-- ---------------------------------------------------
-- 4. Verificar que no queden NULLs
-- ---------------------------------------------------
SELECT COUNT(*) AS faltantes
  FROM RegistrosLevantamientos
 WHERE id_usuario IS NULL;


-- ---------------------------------------------------
-- 5. Forzar NOT NULL y añadir clave foránea sobre Usuarios
-- ---------------------------------------------------
ALTER TABLE RegistrosLevantamientos
  MODIFY COLUMN id_usuario INT NOT NULL;

ALTER TABLE RegistrosLevantamientos
  ADD CONSTRAINT fk_rl_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES Usuarios(id_usuario)
    ON DELETE CASCADE
    ON UPDATE CASCADE;


ALTER TABLE RegistrosLevantamientos
  MODIFY COLUMN id_entrenamiento INT NULL;
