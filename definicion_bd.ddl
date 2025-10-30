-- ==============================
-- Tabla Usuario (CustomUser) 
-- ==============================
CREATE TABLE Usuario (
id INTEGER PRIMARY KEY AUTOINCREMENT,
password VARCHAR(128) NOT NULL,
last_login DATETIME NULL,
is_superuser BOOLEAN NOT NULL DEFAULT 0,
username VARCHAR(150) NOT NULL UNIQUE,
first_name VARCHAR(150) NOT NULL DEFAULT '',
last_name VARCHAR(150) NOT NULL DEFAULT '',
email VARCHAR(254) NOT NULL DEFAULT '',
is_staff BOOLEAN NOT NULL DEFAULT 0,
is_active BOOLEAN NOT NULL DEFAULT 1,
date_joined DATETIME NOT NULL,
us_nombre VARCHAR(100) NOT NULL,
puntaje_total INTEGER DEFAULT 0
);

-- ==============================
-- Tabla Categoria (relacion uno a muchos entre Categoria y Reto)
-- ==============================
CREATE TABLE Categoria (
id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
ca_nombre VARCHAR(100) NOT NULL UNIQUE,
descripcion TEXT NULL
);

-- ==============================
-- Tabla Dificultad (relacion uno a muchos entre Dificultad y Reto)
-- ==============================
CREATE TABLE Dificultad (
id_dificultad INTEGER PRIMARY KEY AUTOINCREMENT,
di_nombre VARCHAR(50) NOT NULL UNIQUE,
puntaje INTEGER DEFAULT 10,
orden SMALLINT DEFAULT 1
);

-- ==============================
-- Tabla Reto (relacion uno a muchos entre Reto y Respuesta)
-- ==============================
CREATE TABLE Reto (
id_reto INTEGER PRIMARY KEY AUTOINCREMENT,
re_dificultad_id INTEGER NOT NULL,
re_categoria_id INTEGER NULL,
re_nombre VARCHAR(200) NOT NULL,
re_descripcion TEXT NOT NULL,
respuesta_reto VARCHAR(200) NOT NULL,
intentos INTEGER DEFAULT 3,
FOREIGN KEY (re_dificultad_id) REFERENCES Dificultad(id_dificultad),
FOREIGN KEY (re_categoria_id) REFERENCES Categoria(id_categoria)
);

-- ==============================
-- Tabla Respuesta (relacion uno a muchos entre Usuario y Respuesta)
-- ==============================
CREATE TABLE Respuesta (
id INTEGER PRIMARY KEY AUTOINCREMENT,
res_usuario_id INTEGER NOT NULL,
res_reto_id INTEGER NOT NULL,
respuesta_usuario VARCHAR(200) NOT NULL,
respuesta_correcta BOOLEAN DEFAULT 0,
puntaje INTEGER DEFAULT 0,
intento SMALLINT DEFAULT 1,
FOREIGN KEY (res_usuario_id) REFERENCES Usuario(id),
FOREIGN KEY (res_reto_id) REFERENCES Reto(id_reto)
);

-- ==============================
-- Tabla HistorialPuntaje (relacion uno a muchos entre Usuario y HistorialPuntaje)
-- ==============================
CREATE TABLE HistorialPuntaje (
id INTEGER PRIMARY KEY AUTOINCREMENT,
usuario_id INTEGER NOT NULL,
puntos INTEGER NOT NULL,
FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
);

-- ==============================
-- Tabla Ranking (relacion uno a uno entre Ranking y Usuario)
-- ==============================
CREATE TABLE Ranking (
id_ranking INTEGER PRIMARY KEY AUTOINCREMENT,
ra_usuario_id INTEGER NOT NULL,
puntaje INTEGER NOT NULL,
FOREIGN KEY (ra_usuario_id) REFERENCES Usuario(id)
);
