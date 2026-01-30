#!/bin/bash
set -e

echo "Starting NEODEMO2 Pipeline..."

# Activate venv if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Run with test image
echo "Processing test image..."
export INPUT_FILE="data/raw/test_image.png"
python3 src/main.py

# Run with PDF if exists
if [ -f "data/raw/financial_report.pdf" ]; then
    echo "Processing financial report..."
    export INPUT_FILE="data/raw/financial_report.pdf"
    python3 src/main.py
fi

echo "Pipeline execution finished successfully."