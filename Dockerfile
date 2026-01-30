# Base image for Python applications
FROM python:3.12-slim

# Install system dependencies for PDF processing and OpenCV
RUN apt-get update && apt-get install -y \
    poppler-utils \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and data folders
COPY src/ ./src/
COPY data/ ./data/
COPY .env .

# Set environment variables
ENV PYTHONPATH=/app

# Default command
CMD ["python", "src/main.py"]