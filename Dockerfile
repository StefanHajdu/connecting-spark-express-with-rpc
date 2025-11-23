# --- Frontend build stage ---
FROM node:20-alpine AS frontend-build
WORKDIR /client_app
COPY client_app/ ./
RUN npm install && npm run build

# --- Backend build stage ---
FROM python:3.11-slim


WORKDIR /home/outline

# Frontend
COPY --from=frontend-build /client_app/build /home/outline/client_app/build

# uv installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# spark_api
WORKDIR /home/outline/spark_api
COPY spark_api ./

# backend
WORKDIR /home/outline/service
COPY service ./


EXPOSE 4444 50051
WORKDIR /home/outline/
COPY start-backend.sh ./

WORKDIR /home/outline/data
VOLUME /home/outline/data

CMD ["./start-backend.sh"]