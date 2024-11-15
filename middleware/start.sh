#!/bin/bash
echo "Ejecutando app.py"
python3 /app/app.py
echo "Iniciando cron"
cron -f