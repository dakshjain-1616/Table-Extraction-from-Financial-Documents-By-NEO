import os
import subprocess

def get_package_version(package_name):
    try:
        result = subprocess.run(['pip', 'show', package_name], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if line.startswith('Version:'):
                return line.split(': ')[1]
    except:
        pass
    return "0.0.1" # Fallback

def create_requirements():
    packages = ['reportlab', 'pandas', 'numpy', 'pillow', 'python-dateutil', 'pytz']
    with open('/Users/dakshjain/Desktop/GitHubDemos/NEODEMO2/requirements.txt', 'w') as f:
        for pkg in packages:
            ver = get_package_version(pkg)
            f.write(f"{pkg}=={ver}\n")
    print("requirements.txt created.")

def create_dockerfile():
    content = """# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (e.g., for reportlab/pillow if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Environment variable to ensure python output is sent to terminal
ENV PYTHONUNBUFFERED=1

# Run the main script
CMD ["python", "src/main.py"]
"""
    with open('/Users/dakshjain/Desktop/GitHubDemos/NEODEMO2/Dockerfile', 'w') as f:
        f.write(content)
    print("Dockerfile created.")

def create_env():
    content = """# Project Configuration
PROJECT_NAME=Financial-OCR-Pipeline
ENVIRONMENT=development

# Path Settings
DATA_DIR=./data/raw
OUTPUT_DIR=./data/processed

# OCR Settings
OCR_CONFIDENCE_THRESHOLD=0.8
MAX_PAGES_TO_PROCESS=10

# Security (Placeholders)
# API_KEY=your_key_here
"""
    with open('/Users/dakshjain/Desktop/GitHubDemos/NEODEMO2/.env', 'w') as f:
        f.write(content)
    print(".env created.")

def create_dockerignore():
    content = """venv/
__pycache__/
*.pyc
.env
.git/
data/processed/
"""
    with open('/Users/dakshjain/Desktop/GitHubDemos/NEODEMO2/.dockerignore', 'w') as f:
        f.write(content)
    print(".dockerignore created.")

if __name__ == "__main__":
    create_requirements()
    create_dockerfile()
    create_env()
    create_dockerignore()