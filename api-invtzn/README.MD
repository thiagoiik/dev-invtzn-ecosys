# API INVTZN (Core Business API)

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Django](https://img.shields.io/badge/Django-6.0-green.svg)
![DRF](https://img.shields.io/badge/DRF-red.svg)
![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)

Esta es la API central (Core) encargada de manejar la lógica de negocio del ecosistema de invitaciones online (INVTZN). Este microservicio no maneja el inicio de sesión ni registro de contraseñas, sino que delega la autenticación a un microservicio externo (`api-auth`) mediante tokens JWT.

---

## 🏗 Arquitectura y Módulos Principales

El proyecto está dividido en aplicaciones (apps) que representan dominios específicos del negocio:

- **`profiles`**: Gestión de perfiles de usuario, roles (ADMIN, VENDOR, CLIENT), finanzas (comisiones) y la billetera digital (`current_balance`).
- **`events`**: Gestión de los eventos (Bodas, XV Años, etc.) asociados a los perfiles de usuario, logística de fechas y ubicaciones.
- **`inventory`**: Catálogo de productos disponibles (digitales, físicos, servicios) y vinculación con *Templates* (componentes Vue) para el Frontend.

---

## 📋 Requisitos Previos

Asegúrate de tener instalado en tu máquina local:
- [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/)
- (Opcional) Python 3.11+ para correr los tests o scripts locales.

---

## 🚀 Instalación y Despliegue Local

Dado que el proyecto utiliza Docker, levantar el entorno completo (incluyendo la base de datos PostgreSQL y la aplicación Django) es cuestión de un solo comando:

1. Clona el repositorio y entra al directorio:
   ```bash
   cd api-invtzn
   ```

2. Construye y levanta los contenedores:
   ```bash
   docker-compose up --build
   ```

El servidor estará corriendo en **http://localhost:8000** (o el puerto configurado en tu `docker-compose.yml`).

---

## 📚 Documentación de la API

Este proyecto implementa auto-documentación utilizando `drf-yasg` (Swagger). Una vez que el servidor esté corriendo, puedes explorar, probar e interactuar visualmente con todos los endpoints de la API visitando:

- **Swagger UI (Recomendado):** [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- **ReDoc (Documentación estática):** [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

*Nota: Para probar endpoints privados en Swagger, haz clic en el botón **"Authorize"** y pega un token JWT válido generado por tu microservicio de autenticación.*

---

## 🧪 Pruebas Automatizadas (Testing)

El ecosistema de pruebas está configurado con **Pytest**, **Pytest-Django** y bases de datos locales en memoria (SQLite) para garantizar la máxima velocidad sin alterar los permisos de tu base de datos de Docker.

Para ejecutar todas las pruebas automatizadas de la API:

1. Entra a la consola de tu contenedor Django (o en tu entorno local activado):
   ```bash
   docker-compose exec web bash
   # o su equivalente dependiendo de cómo se llame tu servicio en docker-compose.yml
   ```

2. Ejecuta Pytest:
   ```bash
   pytest
   ```
   
El sistema detectará automáticamente todos los archivos `tests.py` y correrá las pruebas asegurando que no haya regresiones en la lógica de negocio (ej. validando las *signals* que calculan los saldos en `WalletLog`).

---

## 🔐 Autenticación (Microservicio JWT)

Todo endpoint protegido validará la existencia del header de autorización:
```http
Authorization: Bearer <TU_JWT_TOKEN>
```
La lógica de validación se encuentra en `invtzn_core/authentication.py`, la cual decodifica el JWT, verifica la firma utilizando el `SECRET_KEY` compartido, e inyecta dinámicamente un usuario autenticado a la petición.

---

## 🛠️ Buenas Prácticas de Producción y Seguridad

Este servicio implementa directivas recomendadas de endurecimiento (hardening) para producción:

### 1. Inmutabilidad y usuario sin home (`--no-create-home`)
* **Medida:** El usuario de sistema `django-user` se crea en el Dockerfile con la opción `--no-create-home`.
* **Propósito:** Mantener el sistema de archivos del contenedor lo más libre de directorios de escritura innecesarios y protegerlo bajo el principio de menor privilegio.

### 2. Desactivación del Socket de Gunicorn (`--no-control-socket`)
* **Medida:** Se pasa la opción `--no-control-socket` en la ejecución de Gunicorn en todos los entornos.
* **Propósito:** Previene que Gunicorn intente crear sockets Unix en el home inexistente del usuario. Al correr dentro de Docker, la orquestación y el monitoreo de los contenedores se resuelven en la capa superior (Docker Compose/Kubernetes), por lo que el socket de control de Gunicorn es innecesario.