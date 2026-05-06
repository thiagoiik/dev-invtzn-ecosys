# ==========================================
# Etapa 1: Construcción (Builder)
# ==========================================
FROM python:3.11-slim as builder

WORKDIR /app

# Evita que Python escriba archivos .pyc y fuerza el output directo a la terminal
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependencias del sistema necesarias para compilar paquetes como psycopg2
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copiar solo el archivo de requerimientos para aprovechar el caché de Docker
COPY requirements.txt .

# Compilar las dependencias de Python en formato 'wheel' para transferirlas
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# ==========================================
# Etapa 2: Producción (Runtime)
# ==========================================
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar estrictamente las librerías dinámicas necesarias para la ejecución (ej. PostgreSQL)
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

# Transferir los binarios precompilados desde la Etapa 1 e instalarlos
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copiar el código fuente del proyecto
COPY . .

# Seguridad: Crear un usuario sin privilegios de root para ejecutar la aplicación
RUN adduser --disabled-password --no-create-home django-user && \
    chown -R django-user:django-user /app

# El comando de ejecución (CMD) se omite aquí porque ya está definido en el compose.yml
# EXPOSE 8000 es informativo
USER django-user

EXPOSE 8000