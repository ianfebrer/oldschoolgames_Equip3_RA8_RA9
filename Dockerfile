# Usa una imagen oficial de Python ligera
FROM python:3.11-slim

# Evita que Python genere archivos .pyc y permite que los logs salgan directos
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias para mysqlclient (si usas MySQL)
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos de requerimientos e instala dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código del proyecto
COPY . .

# Expone el puerto donde corre Flask
EXPOSE 5000

# Comando para arrancar la aplicación usando Gunicorn (más estable para producción)
# Si prefieres el modo dev de Flask, usa: CMD ["python", "run.py"]
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.app:app"]
