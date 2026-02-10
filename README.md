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

## 🔧 Extending with NEO
You can enhance and customize this OCR pipeline using **NEO**, an AI-powered development assistant that helps you build, debug, and extend your code.

### Getting Started with NEO

1. **Install the NEO VS Code Extension**
   
   Download and install NEO from the Visual Studio Code Marketplace:
   
   [**NEO VS Code Extension**](https://marketplace.visualstudio.com/items?itemName=NeoResearchInc.heyneo)

2. **Open Your Project in VS Code**
   
   Open this OCR pipeline project in VS Code with the NEO extension installed.

3. **Use NEO to Extend Functionality**
   
   NEO can help you with various extensions and improvements:
   
   - **Add new document formats**: Ask NEO to add support for Word documents, Excel spreadsheets, or other formats
   - **Integrate custom models**: Request NEO to help integrate alternative OCR models or fine-tune existing ones
   - **Build custom post-processing**: Have NEO create specialized validators for specific financial document types
   - **Enhance error handling**: Ask NEO to implement robust error recovery and logging mechanisms
   - **Create API endpoints**: Request NEO to build a REST API wrapper around the pipeline

4. **Example NEO Prompts**
   
   Try these prompts with NEO to extend the pipeline:
```
   "Add support for processing Excel files with embedded tables"
   
   "Create a confidence-based retry mechanism for low-quality OCR results"
   
   "Build a Flask API endpoint that accepts file uploads and returns JSON results"
   
   "Add multi-language support for OCR using alternative TrOCR models"
   
   "Implement parallel processing for batch document conversion"
```

5. **Iterate and Refine**
   
   Use NEO's conversational interface to refine the generated code, ask for explanations, and debug any issues that arise during development.

### Learn More About NEO

Visit [heyneo.so](https://heyneo.so/) to explore additional features and documentation.

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

## 🐋 Deployment & Setup
### Docker Deployment
The project includes a `Dockerfile` for easy containerization.
```bash
# Build the image
docker build -t financial-ocr-pipeline .

# Run the container
docker run --env-file .env financial-ocr-pipeline
```

### Automated Pipeline
You can use the provided shell script to run the full pipeline in your local environment.
```bash
# Make the script executable
chmod +x run_pipeline.sh

# Execute the pipeline
./run_pipeline.sh
```

## 📄 License
MIT License

## 📊 Optimization & Validation (v2.0)
The pipeline has been enhanced with several advanced features to improve accuracy and reliability:

- **Advanced Image Preprocessing**: Integrated OpenCV for denoising, adaptive thresholding (Otsu), and automatic deskewing to prepare documents for OCR.
- **OCR Logic Optimization**: Implemented **Beam Search** (num_beams=5) in the TrOCR engine to produce higher-quality text sequences and more accurate confidence scores.
- **Validation Framework**: Added a validation module that flags low-confidence cell extractions based on a configurable threshold (default: 0.85).
- **Automated Quality Reports**: The evaluator now generates a detailed PDF report including average confidence metrics and validation statuses.
