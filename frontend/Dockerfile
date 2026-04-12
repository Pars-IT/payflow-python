# build stage
FROM node:20 AS builder

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

COPY frontend/. .
RUN npm run build

# production stage (nginx)
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

# optional: custom config
COPY docker/nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]