### 1. Crear el usuario y la base de datos

Primero, creamos el "dueño" de la base de datos y la base de datos misma.
-- 1. Crear el usuario (reemplaza 'tu_usuario_api' y 'tu_password_segura')
CREATE USER auth_service_user WITH PASSWORD 'auth_password_secure';

-- 2. Crear la base de datos asignándola al nuevo usuario
CREATE DATABASE auth_db_service OWNER auth_service_user;

-- 3. (Opcional pero recomendado) Conectarse a la base de datos nueva
\c auth_db_service


### 2. Configurar el esquema y privilegios

Django necesita permisos totales dentro de su propia base de datos para realizar migraciones y gestionar tablas.

-- 4. Asegurar que el usuario tenga todos los privilegios sobre la base de datos
GRANT ALL PRIVILEGES ON DATABASE auth_db_service TO auth_service_user;

-- 5. Conectado a la base de datos, otorgar permisos sobre el esquema 'public'
-- Esto es fundamental para que DRF pueda crear las tablas de auth_user, etc.
GRANT ALL ON SCHEMA public TO auth_service_user;

-- 6. Garantizar permisos sobre futuras tablas y secuencias (muy importante)
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO auth_service_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO auth_service_user;


### 3. Restricciones de Seguridad (Buenas Prácticas)

Si quieres que este usuario sea **solo** para la API y no pueda hacer otras operaciones críticas en el servidor:

-- 7. Limitar al usuario para que no sea superusuario ni pueda crear más roles
ALTER USER auth_service_user NOSUPERUSER NOCREATEDB NOCREATEROLE;


CREATE USER auth_service_user WITH PASSWORD 'auth_password_secure';
CREATE DATABASE auth_db_service OWNER auth_service_user;
\c auth_db_service
GRANT ALL PRIVILEGES ON DATABASE auth_db_service TO auth_service_user;
GRANT ALL ON SCHEMA public TO auth_service_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO auth_service_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO auth_service_user;
ALTER USER auth_service_user NOSUPERUSER NOCREATEDB NOCREATEROLE;