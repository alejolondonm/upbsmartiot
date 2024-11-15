#!/bin/bash

# Crear la red compartida (si no existe)
if ! docker network ls | grep -q shared_network; then
    echo "Creating shared network..."
    docker network create shared_network
fi

# Iniciar el middleware
echo "Starting middleware services..."
cd middleware
docker-compose up -d

# Esperar un momento para asegurar que la base de datos esté lista
echo "Waiting for database to be ready..."
sleep 10

# Iniciar el frontend
echo "Starting frontend services..."
cd ../frontend
docker-compose up -d

echo "All services have been started!"