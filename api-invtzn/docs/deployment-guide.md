# 🚀 Guía de Despliegue en Producción: AWS & Google Cloud

Esta guía técnica documenta el proceso paso a paso para desplegar un servidor en producción utilizando **Amazon Web Services (AWS)** o **Google Cloud Platform (GCP)**. Cubre desde la creación de la máquina virtual (VM) hasta la instalación de Docker, el endurecimiento de seguridad (hardening) y las configuraciones de producción listas para recibir aplicaciones en contenedores de manera segura y escalable.

---

## 🗺️ Diagrama de Flujo del Despliegue (Mermaid)

El siguiente flujo representa visualmente cada una de las fases del despliegue, desde la infraestructura en la nube hasta un entorno listo con SSL y Docker en producción.

```mermaid
graph TD
    %% Styling and colors
    classDef cloud fill:#232F3E,stroke:#FF9900,stroke-width:2px,color:#fff;
    classDef os fill:#E95420,stroke:#fff,stroke-width:1px,color:#fff;
    classDef security fill:#D80027,stroke:#fff,stroke-width:1px,color:#fff;
    classDef docker fill:#2496ED,stroke:#fff,stroke-width:2px,color:#fff;
    classDef prod fill:#2D3748,stroke:#4A5568,stroke-width:1px,color:#fff;
    classDef decision fill:#805AD5,stroke:#fff,stroke-width:1px,color:#fff;

    Start([Inicio del Despliegue]) --> ChooseCloud{¿Qué Cloud Usar?}:::decision
    
    %% AWS Branch
    ChooseCloud -- AWS --> AWS_EC2[1.1. Proveer Instancia EC2<br>- Ubuntu 22.04 / 24.04 LTS<br>- Tipo: t3.micro/small]:::cloud
    AWS_EC2 --> AWS_SG[1.2. Configurar Security Group<br>- Inbound: 22 SSH, 80 HTTP, 443 HTTPS<br>- Outbound: Todo permitido]:::cloud
    AWS_SG --> AWS_Key[1.3. Generar y Descargar Key Pair .pem]:::cloud
    
    %% GCP Branch
    ChooseCloud -- Google Cloud --> GCP_GCE[2.1. Proveer Instancia VM<br>- Compute Engine<br>- Ubuntu 22.04 / 24.04 LTS]:::cloud
    GCP_GCE --> GCP_FW[2.2. Configurar Reglas de Red VPC<br>- Habilitar checks: HTTP / HTTPS<br>- Permitir puerto 22 SSH]:::cloud
    GCP_FW --> GCP_SSH[2.3. Agregar Claves SSH en Metadata del Proyecto]:::cloud

    %% Common OS Initialization
    AWS_Key --> Conn[3. Conexión SSH al Servidor<br>ssh -i clave.pem usuario@ip]:::os
    GCP_SSH --> Conn
    
    Conn --> OS_Init[4. Inicialización del OS<br>sudo apt update && sudo apt upgrade -y]:::os
    OS_Init --> OS_Hardening[5. Hardening de Seguridad<br>- Crear usuario no-root 'deployer'<br>- Asignar permisos sudo<br>- Configurar UFW Firewall<br>- Deshabilitar login root por SSH<br>- Instalar fail2ban]:::security

    %% Docker Setup
    OS_Hardening --> Dock_Clean[6. Remover versiones antiguas de Docker<br>sudo apt-get remove docker docker.io...]:::docker
    Dock_Clean --> Dock_GPG[7. Instalar Llaves GPG y Repositorio Oficial]:::docker
    Dock_GPG --> Dock_Install[8. Instalar Docker Engine, CLI y Compose<br>docker-ce docker-compose-plugin]:::docker
    Dock_Install --> Dock_Group[9. Configurar Grupo Docker para el Usuario<br>sudo usermod -aG docker deployer]:::docker
    Dock_Group --> Dock_Verify[10. Verificar Instalación<br>docker run hello-world]:::docker

    %% Production Ready Configurations
    Dock_Verify --> Prod_Dir[11. Estructura de Directorios<br>Crear /var/www/ecosys-api<br>Asignar dueño a deployer]:::prod
    Prod_Dir --> Prod_Logs[12. Rotación de Logs de Docker<br>Configurar /etc/docker/daemon.json<br>max-size: 10m, max-file: 3]:::prod
    Prod_Logs --> Prod_Env[13. Variables de Entorno<br>Crear archivo .env en producción]:::prod
    Prod_Env --> Prod_Git[14. Git Deploy Keys<br>Generar clave SSH e importar en GitHub]:::prod
    Prod_Git --> Prod_Compose[15. Configurar Docker Compose<br>- restart: unless-stopped<br>- docker compose up -d]:::prod
    Prod_Compose --> Prod_Proxy[16. Servidor Web y Certificados SSL<br>- Instalar Nginx / Caddy<br>- Certbot para HTTPS automático]:::prod
    Prod_Proxy --> End([Servidor en Producción Listo y Seguro])
```

---

## 🛠️ Fase 1: Aprovisionamiento de Infraestructura

Dependiendo del proveedor en la nube seleccionado, realiza la configuración inicial:

### Opción A: Amazon Web Services (AWS) - EC2
1. **Lanzar Instancia (Launch Instance)**:
   - **AMI**: Selecciona `Ubuntu Server 22.04 LTS` o `Ubuntu Server 24.04 LTS` (x86_64 o ARM64 según presupuesto).
   - **Tipo de Instancia**: `t3.small` o `t3.medium` (mínimo recomendado para Docker en producción con múltiples contenedores).
2. **Security Group (Grupo de Seguridad)**:
   - Configura las siguientes reglas de entrada (**Inbound Rules**):
     
     | Tipo | Puerto | Protocolo | Origen | Propósito |
     | :--- | :--- | :--- | :--- | :--- |
     | **SSH** | 22 | TCP | `Mi IP` (o `0.0.0.0/0`) | Acceso seguro SSH |
     | **HTTP** | 80 | TCP | `0.0.0.0/0`, `::/0` | Tráfico web no cifrado |
     | **HTTPS** | 443 | TCP | `0.0.0.0/0`, `::/0` | Tráfico web seguro SSL/TLS |
3. **Key Pair (Claves de Acceso)**:
   - Crea un nuevo par de claves RSA o ED25519 y descarga el archivo `.pem`.
   - Asigna los permisos correctos en tu máquina local antes de conectarte:
     ```bash
     chmod 400 tu-clave.pem
     ```

---

### Opción B: Google Cloud Platform (GCP) - Compute Engine
1. **Crear Instancia de VM**:
   - **Región**: Selecciona la más cercana a tus usuarios.
   - **Tipo de máquina**: Familia de uso general, por ejemplo, `e2-small` o `e2-medium`.
   - **Disco de arranque**: Cambia a `Ubuntu Server 22.04 LTS` o `Ubuntu Server 24.04 LTS` (Tipo: SSD persistente de al menos 20GB).
2. **Reglas de Cortafuegos (Firewall)**:
   - En la sección **Firewall**, marca los siguientes checks:
     - [x] **Permitir tráfico HTTP**
     - [x] **Permitir tráfico HTTPS**
3. **Llaves SSH**:
   - GCP administra las claves SSH de forma nativa a través de `gcloud` o puedes agregarlas manualmente en **Metadatos de Compute Engine -> Claves SSH**.

---

## 🔒 Fase 2: Conexión, Inicialización y Hardening de Seguridad

Conéctate a tu servidor mediante SSH:

```bash
# Para AWS EC2 (el usuario por defecto suele ser 'ubuntu')
ssh -i tu-clave.pem ubuntu@IP_PUBLICA_DEL_SERVIDOR

# Para GCP Compute Engine (el usuario depende de tu clave configurada o cuenta)
ssh -i tu-clave.pem deployer@IP_PUBLICA_DEL_SERVIDOR
```

Una vez dentro, ejecuta los siguientes pasos para asegurar la máquina:

### 1. Actualizar el Sistema Operativo
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Instalar Utilidades Esenciales y Fail2ban
```bash
sudo apt install -y curl git ufw fail2ban software-properties-common apt-transport-https ca-certificates
```

### 3. Crear Usuario de Despliegue (`deployer`)
Evita siempre usar `root` o el usuario por defecto de la nube para operaciones diarias.
```bash
# Crear el nuevo usuario
sudo adduser deployer

# Añadirlo al grupo sudo
sudo usermod -aG sudo deployer
```

### 4. Configurar el Firewall Local (UFW)
```bash
# Definir reglas por defecto
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Permitir SSH, HTTP y HTTPS
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Habilitar el cortafuegos
sudo ufw enable
```

### 5. Asegurar el Servicio SSH
Modifica las configuraciones de SSH para evitar ataques de fuerza bruta.
```bash
sudo nano /etc/ssh/sshd_config
```
Busca y configura las siguientes líneas (si no existen, agrégalas):
```text
PermitRootLogin no
PasswordAuthentication no
```
Guarda el archivo (`Ctrl + O`, `Enter`, `Ctrl + X`) y reinicia el servicio SSH:
```bash
sudo systemctl restart ssh
```
> [!IMPORTANT]
> **No cierres tu sesión SSH actual** hasta abrir una nueva consola y comprobar que puedes acceder exitosamente con el nuevo usuario `deployer` usando tu clave pública.

---

## 🐳 Fase 3: Instalación de Docker y Docker Compose

Instalaremos la versión oficial y actualizada de Docker en lugar de los paquetes antiguos incluidos en los repositorios por defecto de Ubuntu.

### 1. Eliminar versiones previas no oficiales
```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

### 2. Configurar el repositorio oficial de Docker
```bash
# Agregar la clave GPG oficial de Docker
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Añadir el repositorio a las fuentes de Apt
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Actualizar el índice de paquetes
sudo apt update
```

### 3. Instalar componentes de Docker
```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 4. Configurar permisos para ejecutar Docker sin `sudo`
```bash
# Añadir tu usuario al grupo docker
sudo usermod -aG docker deployer

# Activar el cambio de grupo inmediatamente en la sesión actual
newgrp docker
```

### 5. Habilitar el inicio automático de Docker en el arranque del sistema
```bash
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
```

### 6. Validar que Docker funcione correctamente
```bash
docker run hello-world
docker compose version
```

---

## ⚙️ Fase 4: Configuración de Docker para Producción

Antes de desplegar tu contenedor, es fundamental configurar Docker para evitar problemas comunes en producción, como quedarse sin espacio en disco debido a logs infinitos.

### 1. Rotación de Logs de Contenedores
Por defecto, Docker acumula los logs de los contenedores indefinidamente. Vamos a limitar esto a un tamaño máximo de 10 megabytes por archivo y un máximo de 3 archivos rotativos por contenedor.

Crea o edita el archivo `/etc/docker/daemon.json`:
```bash
sudo nano /etc/docker/daemon.json
```
Agrega la siguiente configuración:
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```
Reinicia el servicio de Docker para aplicar los cambios:
```bash
sudo systemctl restart docker
```

### 2. Estructura de Directorios para tus Aplicaciones
Crea una carpeta organizada para los archivos del proyecto (por ejemplo, en `/var/www/`):
```bash
sudo mkdir -p /var/www/ecosys-api
sudo chown -R deployer:deployer /var/www/ecosys-api
cd /var/www/ecosys-api
```

### 3. Generar y Configurar Deploy Keys para Git
Para clonar de forma segura tus repositorios privados sin exponer tus credenciales personales, utiliza una clave SSH de despliegue específica para el servidor.

```bash
# Generar clave SSH
ssh-keygen -t ed25519 -C "server-deployer@ecosys" -N "" -f ~/.ssh/id_ed25519

# Mostrar la clave pública para copiarla
cat ~/.ssh/id_ed25519.pub
```
1. Copia la salida del comando.
2. Ve a tu repositorio de GitHub/GitLab -> **Settings** -> **Deploy Keys** -> **Add Deploy Key**.
3. Pega la clave, dale un nombre descriptivo (ej: `Servidor AWS Produccion`) y déjala con permisos de solo lectura (read-only).
4. Clona tu proyecto:
   ```bash
   git clone git@github.com:tu-usuario/tu-repositorio.git .
   ```

### 4. Configurar Variables de Entorno (`.env`)
Nunca subas credenciales o claves secretas a Git. Crea el archivo localmente en el servidor:
```bash
nano .env
```
Define tus variables necesarias para producción:
```env
DEBUG=False
SECRET_KEY=tu-clave-secreta-ultrasegura
DATABASE_URL=postgres://usuario:password@db-host:5432/db-name
ALLOWED_HOSTS=tuservidor.com,IP_DEL_SERVIDOR
```

---

## 🛡️ Fase 5: Exponer la Aplicación de forma Segura (Reverse Proxy + SSL)

Aunque tus contenedores Docker estén corriendo en puertos como el `8000`, **nunca expongas estos puertos directamente a Internet**. Configura un proxy inverso como **Nginx** para manejar la seguridad, el SSL y delegar el tráfico al contenedor de Docker.

### 1. Instalar Nginx y Certbot
```bash
sudo apt install -y nginx certbot python3-certbot-nginx
```

### 2. Configurar el Bloque de Servidor (VirtualHost) en Nginx
Crea un archivo de configuración para tu sitio:
```bash
sudo nano /etc/nginx/sites-available/ecosys-api
```
Copia y pega la siguiente configuración, reemplazando `tu-dominio.com` con tu dominio real:
```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Carpeta de archivos estáticos colectados por Django (opcional si es API pura con staticfiles externos)
    location /static/ {
        alias /var/www/ecosys-api/staticfiles/;
    }
}
```

Habilita la configuración creando un enlace simbólico y reiniciando Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/ecosys-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 3. Generar Certificado SSL Gratis con Let's Encrypt
Asegura tu servidor cifrando todo el tráfico con HTTPS de manera automática:
```bash
sudo certbot --nginx -d tu-dominio.com
```
*Sigue las instrucciones en pantalla, acepta los términos y selecciona la opción de redirigir todo el tráfico HTTP a HTTPS de manera automática.*

---

## 🎉 ¡Listo! Tu Servidor está preparado para Producción

Ahora tienes un servidor endurecido en seguridad, con Docker y Docker Compose listos, rotación de logs activa, cortafuegos configurado y un proxy inverso con SSL (HTTPS) apuntando directamente a tu contenedor. 

Para arrancar tus servicios en segundo plano simplemente ejecuta:
```bash
docker compose up -d
```
Cualquier petición HTTPS a `https://tu-dominio.com` será gestionada por Nginx y redirigida instantáneamente y de forma segura a tus contenedores de Docker.
