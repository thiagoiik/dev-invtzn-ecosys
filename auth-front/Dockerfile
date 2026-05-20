# ETAPA 1: La Fábrica (Build)
FROM node:20-alpine AS builder
WORKDIR /app

# Definir argumentos de construcción para las APIs
ARG VITE_API_AUTH_URL
ARG VITE_API_INVTZN_URL

# Configurar variables de entorno de construcción para Vite
ENV VITE_API_AUTH_URL=$VITE_API_AUTH_URL
ENV VITE_API_INVTZN_URL=$VITE_API_INVTZN_URL

COPY package.json package-lock.json* ./
RUN npm install 
COPY . .
# Aquí se generan los archivos estáticos en /dist
RUN npm run build  

# ETAPA 2: El Servidor (Production)
FROM nginxinc/nginx-unprivileged:alpine
# Copiamos solo lo necesario desde la etapa anterior
COPY --from=builder /app/dist /usr/share/nginx/html
# Copiamos nuestra configuración de Nginx (el fallback para SPA)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]