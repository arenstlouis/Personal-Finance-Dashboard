# 1. Use an official Python image
FROM python:3.12-slim

# 2. Set environment variables (prevents Python from buffering output)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Install system dependencies for Postgres (psycopg2 needs these)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your code
COPY . /app/

# 7. Start the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]