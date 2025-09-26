-- =============================================================================
-- Esquema para la Tabla Maestra de Usuarios en PostgreSQL
-- Se ejecutará en el esquema 'public' de la base de datos principal.
-- =============================================================================

-- Crear la tabla de Usuarios si no existe
CREATE TABLE IF NOT EXISTS public.Usuarios (
    id_usuario          SERIAL PRIMARY KEY,
    nombre_usuario      VARCHAR(100) NOT NULL UNIQUE,
    contrasena_hash     VARCHAR(255) NOT NULL,
    rol                 VARCHAR(20) NOT NULL CHECK(rol IN ('admin', 'superuser')),
    nombre_gym          VARCHAR(100),
    nombre_esquema      VARCHAR(63) UNIQUE, -- El nombre del esquema del tenant (ej. tenant_gym_power)

    -- Restricción para el rol 'admin': debe tener un nombre de gym y un esquema.
    CONSTRAINT chk_admin CHECK (
        (rol = 'admin' AND nombre_gym IS NOT NULL AND nombre_esquema IS NOT NULL) OR (rol <> 'admin')
    ),

    -- Restricción para el rol 'superuser': NO debe tener nombre de gym ni esquema.
    CONSTRAINT chk_superuser CHECK (
        (rol = 'superuser' AND nombre_gym IS NULL AND nombre_esquema IS NULL) OR (rol <> 'superuser')
    )
);

-- Nota: El superusuario se creará a través de un script de inicialización separado
-- para no exponer credenciales en el código fuente.