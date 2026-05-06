# ETAPA 1: La Fábrica (Build)
FROM node:24.13.1 AS builder
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install 
COPY . .
# Aquí se generan los archivos estáticos en /dist
RUN npm run build  

# ETAPA 2: El Servidor (Production)
FROM nginx:alpine
# Copiamos solo lo necesario desde la etapa anterior
COPY --from=builder /app/dist /usr/share/nginx/html
# Copiamos nuestra configuración de Nginx (el fallback para SPA)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]