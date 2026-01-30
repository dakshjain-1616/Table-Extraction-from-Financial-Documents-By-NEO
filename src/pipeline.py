import os
import json
import logging
import pandas as pd
from PIL import Image
try:
    from src.document_loader import DocumentLoader
    from src.table_detector import TableDetector
    from src.ocr_engine import OCREngine
    from src.processor import TableProcessor
except ImportError:
    from document_loader import DocumentLoader
    from table_detector import TableDetector
    from ocr_engine import OCREngine
    from processor import TableProcessor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OCRPipeline:
    def __init__(self):
        self.loader = DocumentLoader()
        self.detector = TableDetector()
        self.ocr = OCREngine()
        self.processor = TableProcessor()

    def process_document(self, file_path):
        logger.info(f"Processing document: {file_path}")
        images = self.loader.load(file_path)
        all_results = []

        for page_num, image in enumerate(images):
            tables = self.detector.detect_tables(image)
            for table_idx, table in enumerate(tables):
                table_box = table['box']
                structure = self.detector.recognize_structure(image, table_box)
                table_image = image.crop(table_box)
                
                cells = [s for s in structure if s['label'] == 'table cells']
                rows = sorted([s for s in structure if s['label'] == 'table row'], key=lambda x: x['box'][1])
                cols = sorted([s for s in structure if s['label'] == 'table column'], key=lambda x: x['box'][0])
                
                processed_cells = []
                for cell in cells:
                    cbox = cell['box']
                    cell_img = table_image.crop(cbox)
                    text, conf = self.ocr.extract_text(cell_img)
                    cx, cy = (cbox[0] + cbox[2])/2, (cbox[1] + cbox[3])/2
                    row_idx = next((i for i, r in enumerate(rows) if r['box'][1] <= cy <= r['box'][3]), -1)
                    col_idx = next((i for i, c in enumerate(cols) if c['box'][0] <= cx <= c['box'][2]), -1)
                    processed_cells.append({'text': text, 'conf': conf, 'row': row_idx, 'col': col_idx, 'box': cbox})
                
                df = self.processor.process_table(processed_cells)
                all_results.append({
                    'page': page_num,
                    'table_index': table_idx,
                    'df': df,
                    'confidence': sum([c['conf'] for c in processed_cells]) / (len(processed_cells) + 1e-6)
                })
        return all_results

    def export(self, results, base_name, output_dir=None, document_id="unknown_doc"):
        """
        Exports results to JSON and CSV with enhanced formatting and strict schema.
        """
        if output_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            output_dir = os.path.join(base_dir, "data", "processed")
        
        os.makedirs(output_dir, exist_ok=True)
        exported_files = []
        
        for i, res in enumerate(results):
            csv_path = os.path.join(output_dir, f"{base_name}_t{i}.csv")
            json_path = os.path.join(output_dir, f"{base_name}_t{i}.json")
            
            # Subtask 2: Enhance CSV generation
            df = res['df']
            # Ensure headers are strings and clean
            df.columns = [str(c).strip().replace('\n', ' ') for c in df.columns]
            df.to_csv(csv_path, index=False, quoting=1) # Quote all non-numeric for cleanliness
            
            # Subtask 1: Strict JSON schema
            all_text = " ".join(df.values.flatten().astype(str))
            
            structured_output = {
                "document_id": document_id,
                "table_id": f"{base_name}_t{i}",
                "extracted_text": all_text.strip(),
                "confidence_score": round(res['confidence'], 4),
                "metadata": {
                    "page_number": res['page'],
                    "table_index_on_page": res['table_index'],
                    "row_count": len(df),
                    "column_count": len(df.columns),
                    "execution_timestamp": pd.Timestamp.now().isoformat()
                },
                "structured_data": df.to_dict(orient='records')
            }
            
            with open(json_path, 'w') as f:
                json.dump(structured_output, f, indent=4)
                
            exported_files.extend([csv_path, json_path])
            
        return exported_files

if __name__ == "__main__":
    pipeline = OCRPipeline()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    test_img_path = os.path.join(base_dir, "data", "raw", "test_image.png")
    if os.path.exists(test_img_path):
        results = pipeline.process_document(test_img_path)
        files = pipeline.export(results, "smoke_test")
        print(f"Pipeline test complete. Exported files: {files}")
    else:
        print(f"Test image not found at {test_img_path}")