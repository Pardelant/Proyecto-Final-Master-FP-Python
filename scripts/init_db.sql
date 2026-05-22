-- Aseguramos que la base de datos use codificación UTF-8 moderna
ALTER DATABASE `escuela-bd` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE `escuela-bd`;

-- Configuramos las tablas con soporte nativo para tildes y eñes
CREATE TABLE IF NOT EXISTS asignaturas (
    nombre VARCHAR(100) PRIMARY KEY
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS alumnos (
    dni VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS profesores (
    dni VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    especialidad VARCHAR(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS notas_alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_dni VARCHAR(20),
    asignatura_nombre VARCHAR(100),
    nota DECIMAL(4, 2) DEFAULT 0.0 CHECK (
        nota >= 0 AND nota <= 10
    ),
    FOREIGN KEY (alumno_dni) REFERENCES alumnos(dni) ON DELETE CASCADE,
    FOREIGN KEY (asignatura_nombre) REFERENCES asignaturas(nombre) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS asignaturas_profesores (
    profesor_dni VARCHAR(20),
    asignatura_nombre VARCHAR(100),
    PRIMARY KEY (profesor_dni, asignatura_nombre),
    FOREIGN KEY (profesor_dni) REFERENCES profesores(dni) ON DELETE CASCADE,
    FOREIGN KEY (asignatura_nombre) REFERENCES asignaturas(nombre) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(20) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol ENUM('alumno', 'profesor') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- INICIALIZAR DATOS
INSERT INTO asignaturas (nombre)
VALUES ('Programación Python'),
    ('Bases de Datos'),
    ('Desarrollo Web'),
    ('Sistemas Inteligentes');

INSERT INTO profesores (dni, nombre, email, especialidad)
VALUES (
        '12345678P',
        'Guido Van Rossum',
        'guido@escuela.com',
        'Ingeniería de Software'
    ),
    (
        '87654321T',
        'Ada Lovelace',
        'ada@escuela.com',
        'Algoritmia'
    );

INSERT INTO asignaturas_profesores (profesor_dni, asignatura_nombre)
VALUES ('12345678P', 'Programación Python'),
    ('12345678P', 'Bases de Datos'),
    ('87654321T', 'Sistemas Inteligentes');

INSERT INTO alumnos (dni, nombre, email)
VALUES (
        '11122233A',
        'Juan Pérez',
        'juan.perez@correo.com'
    ),
    (
        '44455566B',
        'María García',
        'm.garcia@correo.com'
    ),
    ('77788899C', 'Carlos Ruiz', 'c.ruiz@correo.com');

INSERT INTO notas_alumnos (alumno_dni, asignatura_nombre, nota)
VALUES ('11122233A', 'Programación Python', 8.5),
    ('11122233A', 'Bases de Datos', 7.0),
    ('44455566B', 'Programación Python', 9.2),
    ('44455566B', 'Desarrollo Web', 6.5),
    ('77788899C', 'Sistemas Inteligentes', 4.5);

INSERT INTO usuarios (dni, password, rol)
VALUES ('11122233A', '1234', 'alumno'),
    ('44455566B', '1234', 'alumno'),
    ('77788899C', '1234', 'alumno'),
    ('12345678P', 'admin', 'profesor'),
    ('87654321T', 'admin', 'profesor');