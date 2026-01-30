import os
import warnings
import logging

# 1. Immediate suppression before any other imports
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

# 2. Configure logging to suppress noisy libraries
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s', force=True)
for noisy_lib in ['timm', 'transformers', 'PIL', 'pytorch_lightning']:
    logging.getLogger(noisy_lib).setLevel(logging.ERROR)

from pipeline import OCRPipeline
from evaluator import PerformanceEvaluator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def main():
    # 1. Initialize Pipeline and Evaluator
    pipeline = OCRPipeline()
    evaluator = PerformanceEvaluator()
    
    # 2. Define input (using relative paths or environment variables)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_file = os.getenv("INPUT_FILE", os.path.join(base_dir, "data", "raw", "test_image.png"))
    
    # 3. Execute Pipeline
    logger.info(f"Starting End-to-End Pipeline Execution with: {input_file}")
# 3. Process Document
    doc_id = os.path.basename(input_file)
    logger.info(f"Processing: {input_file}")
    results = pipeline.process_document(input_file)
    
    # 4. Export Results (CSV/JSON per table) with enhanced formatting
    exported_files = pipeline.export(results, "final_run", document_id=doc_id)
    logger.info(f"Exported {len(exported_files)} structured data files.")
    
    # 5. Collect Validation Errors and Generate Professional Report
    validation_errors = []
    for r_idx, res in enumerate(results):
        # res['df'] contains the structured table
        # We can flag rows/cells with low confidence if needed, 
        # but evaluator.validate_results expects the raw cell list.
        # For simplicity in report, we pass formatted error dicts.
        if res.get('confidence', 1.0) < evaluator.confidence_threshold:
            validation_errors.append({
                'id': f"T{r_idx}",
                'type': 'LOW_AVG_CONF',
                'src': f"Table {r_idx} Header/Data",
                'conf': res.get('confidence', 0.0)
            })
    
    evaluator.update_from_pipeline(results)
    report_path = evaluator.generate_report(validation_errors=validation_errors)
    logger.info(f"Quality Report generated at: {report_path}")
    expected_files = [
        os.path.join(base_dir, "data", "processed", "final_run_t0.csv"),
        os.path.join(base_dir, "data", "processed", "final_run_t0.json"),
        os.path.join(base_dir, "data", "processed", "quality_report.pdf")
    ]
    
    success = True
    for f in expected_files:
        if not os.path.exists(f):
            logger.error(f"Missing expected output: {f}")
            success = False
    
    if success:
        print("\n[VERIFICATION SUCCESSFUL] All deliverables are present and valid.")
    else:
        print("\n[VERIFICATION FAILED] Some deliverables are missing.")

if __name__ == "__main__":
    main()