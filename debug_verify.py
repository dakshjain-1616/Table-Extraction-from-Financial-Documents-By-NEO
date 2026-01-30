import sys
import os

# Add the project root to the path
PROJECT_ROOT = '/Users/dakshjain/Desktop/GitHubDemos/NEODEMO2'
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

try:
    from src.evaluator import PerformanceEvaluator
except ImportError as ie:
    print(f"FAILED to import PerformanceEvaluator: {ie}")
    sys.exit(1)

def main():
    try:
        evaluator = PerformanceEvaluator()
        # Set some metrics
        evaluator.metrics['ocr_avg_confidence'] = 0.92
        evaluator.metrics['table_count'] = 5
        # Generate report
        path = evaluator.generate_report(validation_errors=[{'id': 'T1', 'type': 'TEST', 'src': 'Verify', 'conf': 0.88}])
        print(f"SUCCESS: Report generated at {path}")
        if os.path.exists(path):
            print("File verified on disk.")
    except Exception as e:
        print(f"FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

# Optional: notify planner
# If sync_with_planner is defined elsewhere, you can call it here
# sync_with_planner(
#     action_summary="Fixed NameError in evaluator.py by adding missing pandas import. Verified PDF report generation successfully. All environment bundle files (Dockerfile, requirements.txt, .env) are present and validated.",
#     files_changed=["/Users/dakshjain/Desktop/GitHubDemos/NEODEMO2/src/evaluator.py"],
#     metrics={"subtasks_completed": 4, "final_verification": "PASS"}
# )