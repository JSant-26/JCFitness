-- ========================================================
-- Plantilla de Esquema para un Tenant de JCFitness en PostgreSQL
-- ¡¡ATENCIÓN!! Este script es una plantilla. El marcador "{schema_name}"
-- será reemplazado dinámicamente por el nombre del esquema del nuevo cliente.
-- ========================================================
-- Creamos un nuevo esquema para aislar los datos del tenant
CREATE SCHEMA IF NOT EXISTS "{schema_name}";

-- Crear las tablas dentro del nuevo esquema

CREATE TABLE IF NOT EXISTS "{schema_name}".Miembros (
    id_miembro          SERIAL PRIMARY KEY,
    nombre              VARCHAR(100) NOT NULL,
    apellido            VARCHAR(100),
    sexo                VARCHAR(10) CHECK(sexo IN ('Masculino', 'Femenino')),
    telefono            VARCHAR(20),
    plantilla_huella    TEXT, -- Las plantillas pueden ser largas
    fecha_registro      DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS "{schema_name}".Asistencias (
    id_asistencia       SERIAL PRIMARY KEY,
    id_miembro          INTEGER NOT NULL REFERENCES "{schema_name}".Miembros(id_miembro) ON DELETE CASCADE,
    fecha               DATE NOT NULL DEFAULT CURRENT_DATE,
    hora_entrada        TIME,
    hora_salida         TIME,
    UNIQUE (id_miembro, fecha)
);

CREATE TABLE IF NOT EXISTS "{schema_name}".Pagos (
    id_pago             SERIAL PRIMARY KEY,
    id_miembro          INTEGER NOT NULL REFERENCES "{schema_name}".Miembros(id_miembro) ON DELETE CASCADE,
    fecha_pago          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    monto               DECIMAL(10, 2) NOT NULL CHECK(monto > 0)
);

CREATE TABLE IF NOT EXISTS "{schema_name}".Entrenadores (
    id_entrenador       SERIAL PRIMARY KEY,
    nombre              VARCHAR(100) NOT NULL,
    apellido            VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS "{schema_name}".Pagos_Entrenadores (
    id_pago_entrenador  SERIAL PRIMARY KEY,
    id_entrenador       INTEGER NOT NULL REFERENCES "{schema_name}".Entrenadores(id_entrenador) ON DELETE CASCADE,
    fecha_pago          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    monto               DECIMAL(10, 2) NOT NULL CHECK(monto > 0)
);

CREATE TABLE IF NOT EXISTS "{schema_name}".Gastos (
    id_gasto            SERIAL PRIMARY KEY,
    fecha               TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    gasto_admin         DECIMAL(10, 2) DEFAULT 0,
    gasto_aseo          DECIMAL(10, 2) DEFAULT 0,
    total_entrenadores  DECIMAL(10, 2) DEFAULT 0
);


-- Índices para optimizar el rendimiento de las consultas
CREATE INDEX IF NOT EXISTS idx_miembros_nombre_apellido ON "{schema_name}".Miembros(nombre, apellido);
CREATE INDEX IF NOT EXISTS idx_asistencias_fecha ON "{schema_name}".Asistencias(fecha);
CREATE INDEX IF NOT EXISTS idx_pagos_fecha_pago ON "{schema_name}".Pagos(fecha_pago);
CREATE INDEX IF NOT EXISTS idx_pagos_entrenadores_fecha_pago ON "{schema_name}".Pagos_Entrenadores(fecha_pago);

-- Aquí irían las Vistas y Triggers, que en PostgreSQL se definen con funciones
-- y procedimientos almacenados, lo cual podemos añadir en el siguiente paso.