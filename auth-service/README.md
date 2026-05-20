# 🔐 Auth Service (Microservicio de Autenticación)

Este microservicio se encarga de la gestión centralizada de usuarios, perfiles, registro, autenticación y emisión de tokens JWT para el ecosistema **invtzn**.

---

## 🛠️ Buenas Prácticas de Producción y Seguridad

Este servicio implementa políticas de seguridad estrictas recomendadas para entornos de producción:

### 1. Usuario sin privilegios y sin directorio personal (`--no-create-home`)
* **Medida:** El contenedor Docker añade al usuario `django-user` utilizando la bandera `--no-create-home`.
* **Propósito:** Cumplir con el **principio de menor privilegio** y asegurar que el contenedor sea lo más inmutable posible, evitando directorios de escritura innecesarios.

### 2. Desactivación de Socket de Control de Gunicorn (`--no-control-socket`)
* **Medida:** Gunicorn se ejecuta utilizando el parámetro `--no-control-socket` (tanto en desarrollo como en producción).
* **Propósito:** Debido a la inmutabilidad y falta del directorio home del usuario de ejecución, Gunicorn no puede (ni necesita) crear el archivo de socket Unix de control (`gunicorn.ctl`). En entornos dockerizados, el escalado y control de procesos se delegan a Docker/Kubernetes, por lo que este socket es redundante y se desactiva de forma segura.

---

## 🚀 Despliegue Local (Desarrollo)

1. Asegúrate de tener el archivo `.env` en la raíz del ecosistema con las variables correspondientes (`AUTH_DJANGO_SECRET_KEY`, `AUTH_DB_USER`, etc.).
2. Levanta el contenedor desde esta carpeta:
   ```bash
   docker compose up -d --build
   ```
3. Ejecuta las migraciones:
   ```bash
   docker compose exec auth-service-api python manage.py migrate
   ```
