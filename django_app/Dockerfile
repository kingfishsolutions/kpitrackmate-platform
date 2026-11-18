# Use an official lightweight Python 3.12 image
FROM python:3.12-slim

# Prevent Python from writing .pyc files and force unbuffered stdout/stderr logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies needed to compile psycopg (PostgreSQL adapter)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (caches layer if requirements.txt hasn't changed)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of your Django project code into the container
COPY . .

# Expose port 8000 (used by Gunicorn inside the Docker network)
EXPOSE 8000

# Default command (overridden by the command in docker-compose.yml)
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
