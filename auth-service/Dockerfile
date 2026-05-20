# ==========================================
# Etapa 1: Construcción (Builder)
# ==========================================
FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependencias del sistema necesarias para compilar paquetes como psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Se define un argumento para saber qué entorno de requirements instalar (por defecto production)
ARG ENV=production
COPY requirements/ ./requirements/

# Compilar las dependencias de Python en formato 'wheel' para transferirlas
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements/${ENV}.txt

# ==========================================
# Etapa 2: Producción (Runtime)
# ==========================================
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Transferir los binarios precompilados e instalar
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copiar el código fuente del proyecto
COPY . .

# Seguridad: Crear un usuario sin privilegios de root para ejecutar la aplicación
RUN adduser --disabled-password --no-create-home --gecos "" django-user && \
    chown -R django-user:django-user /app

USER django-user

EXPOSE 8000