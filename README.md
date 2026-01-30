# Financial OCR Pipeline: Structured Table Extraction by <a href='https://heyneo.so/' target='_blank'>**NEO**</a>

A high-performance OCR pipeline specialized for extracting structured data from complex financial tables using state-of-the-art Deep Learning models.

## 🚀 Overview

This project provides an end-to-end solution for converting financial documents (PDFs, scans, images) into machine-readable CSV and JSON formats. It leverages:
- **Table Transformer** for precise table detection and structural analysis.
- **Microsoft TrOCR** for cell-level text recognition, handling both printed and handwritten financial terminology.
- **Pandas-based Post-processing** for handling merged cells, data normalization, and schema validation.

## 🏗️ Architecture

1. **Document Loading**: Converts multi-page PDFs or images into a standardized processing format.
2. **Table Detection**: Identifies table boundaries and internal structures (rows/columns) using `microsoft/table-transformer-detection`.
3. **Cell Extraction**: Crops individual cells and applies `microsoft/trocr-base-printed` for high-accuracy OCR.
4. **Data Reconstruction**: Maps OCR results back to a grid structure, resolving merged cells and hierarchical headers.
5. **Export & Validation**: Generates CSV/JSON outputs with confidence scores and anomaly reports.

## 🛠️ Installation

### Prerequisites
- Python 3.12+
- Popolar-utils (for `pdf2image`)

### Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 📖 Usage

### Command Line Interface
```bash
python src/main.py --input data/raw/financial_report.pdf --output data/processed/
```

### Python API
```python
from src.pipeline import OCRPipeline

pipeline = OCRPipeline()
results = pipeline.process_document("path/to/document.png")
pipeline.export(results, "output_name")
```

## 📊 Models
- **Detection**: [Table Transformer (TATR)](https://huggingface.co/microsoft/table-transformer-detection)
- **OCR**: [TrOCR Base Stage 1](https://huggingface.co/microsoft/trocr-base-printed)

## 📁 Export Examples

### JSON Metadata
```json
{
    "page": 0,
    "table_index": 0,
    "avg_ocr_confidence": 0.985,
    "data": {
        "columns": ["Description", "2023", "2022"],
        "data": [["Total Revenue", "1,200.50", "1,100.00"]]
    }
}
```

## 📄 License
MIT License