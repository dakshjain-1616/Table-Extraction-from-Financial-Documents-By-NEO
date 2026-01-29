import torch
from transformers import AutoImageProcessor, TableTransformerForObjectDetection
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TableDetector:
    """Detects tables and recognizes their structure using Table Transformer (TATR)."""
    
    def __init__(self):
        # detection model identifies WHERE tables are
        self.det_model_name = "microsoft/table-transformer-detection"
        # structure model identifies rows, columns, and cells
        self.struct_model_name = "microsoft/table-transformer-structure-recognition"
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
        
        self.det_processor = AutoImageProcessor.from_pretrained(self.det_model_name)
        self.det_model = TableTransformerForObjectDetection.from_pretrained(self.det_model_name).to(self.device)
        
        self.struct_processor = AutoImageProcessor.from_pretrained(self.struct_model_name)
        self.struct_model = TableTransformerForObjectDetection.from_pretrained(self.struct_model_name).to(self.device)

    def detect_tables(self, image, threshold=0.7):
        """Finds table boundaries in the image."""
        inputs = self.det_processor(images=image, return_tensors="pt").to(self.device)
        outputs = self.det_model(**inputs)
        
        target_sizes = torch.tensor([image.size[::-1]]).to(self.device)
        results = self.det_processor.post_process_object_detection(outputs, threshold=threshold, target_sizes=target_sizes)[0]
        
        tables = []
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            # Label 0 is usually 'table' in TATR detection
            box = [round(i, 2) for i in box.tolist()]
            tables.append({
                "box": box,
                "score": score.item(),
                "label": self.det_model.config.id2label[label.item()]
            })
        logger.info(f"Detected {len(tables)} tables.")
        return tables

    def recognize_structure(self, image, table_box, threshold=0.3):
        """Recognizes internal structure (rows/columns) within a cropped table image."""
        # Crop the table from the original image
        table_img = image.crop(table_box)
        
        inputs = self.struct_processor(images=table_img, return_tensors="pt").to(self.device)
        outputs = self.struct_model(**inputs)
        
        target_sizes = torch.tensor([table_img.size[::-1]]).to(self.device)
        results = self.struct_processor.post_process_object_detection(outputs, threshold=threshold, target_sizes=target_sizes)[0]
        
        structure = []
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            label_name = self.struct_model.config.id2label[label.item()]
            box = [round(i, 2) for i in box.tolist()]
            structure.append({
                "box": box,
                "score": score.item(),
                "label": label_name
            })
        return structure

if __name__ == "__main__":
    # Create a small dummy image for smoke test
    test_img = Image.new('RGB', (800, 600), color=(255, 255, 255))
    detector = TableDetector()
    results = detector.detect_tables(test_img)
    print(f"Smoke test successful. Detector initialized.")