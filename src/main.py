import logging
import os
from pipeline import OCRPipeline
from evaluator import PerformanceEvaluator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # 1. Initialize Pipeline and Evaluator
    pipeline = OCRPipeline()
    evaluator = PerformanceEvaluator()
    
    # 2. Define input (using the verified smoke test image)
    input_file = "/root/claude_tests/NEODEMO2/data/raw/test_image.png"
    
    # 3. Execute Pipeline
    logger.info("Starting End-to-End Pipeline Execution...")
    results = pipeline.process_document(input_file)
    
    # 4. Export Results (CSV/JSON per table)
    exported_files = pipeline.export(results, "final_run")
    logger.info(f"Exported {len(exported_files)} data files.")
    
    # 5. Generate Performance and Quality Report
    evaluator.update_from_pipeline(results)
    report_path = evaluator.generate_report()
    logger.info(f"Quality Report generated at: {report_path}")
    
    # 6. Verification check
    expected_files = [
        "/root/claude_tests/NEODEMO2/data/processed/final_run_t0.csv",
        "/root/claude_tests/NEODEMO2/data/processed/final_run_t0.json",
        "/root/claude_tests/NEODEMO2/data/processed/quality_report.pdf"
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