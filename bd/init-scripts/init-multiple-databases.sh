#!/bin/bash
set -e
set -u

function create_user_and_database() {
    local database=$1
    local user=$2
    local password=$3
    echo "  Creando usuario y base de datos: '$database' para el usuario '$user'"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        CREATE USER $user WITH PASSWORD '$password';
        CREATE DATABASE $database;
        GRANT ALL PRIVILEGES ON DATABASE $database TO $user;
        ALTER DATABASE $database OWNER TO $user;
EOSQL
}

if [ -n "${POSTGRES_MULTIPLE_DATABASES:-}" ]; then
    echo "Inicialización de múltiples bases de datos solicitada: $POSTGRES_MULTIPLE_DATABASES"
    for db_info in $(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' '); do
        # Formato esperado: nombre_bd:usuario:contraseña
        IFS=':' read -r dbname dbuser dbpass <<< "$db_info"
        create_user_and_database $dbname $dbuser $dbpass
    done
    echo "Múltiples bases de datos creadas exitosamente."
fi
