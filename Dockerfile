# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables for the virtual environment path
ENV PATH="/opt/venv/bin:$PATH"

# Install system dependencies required for your project (PostgreSQL, Pillow, etc.)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt /app/

# Create a virtual environment and install dependencies
RUN python -m venv /opt/venv
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your project files to the container
COPY . /app/

# Expose the port your Django app will run on (default is 8000)
EXPOSE 8000

# Run Django migrations and start the app
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
