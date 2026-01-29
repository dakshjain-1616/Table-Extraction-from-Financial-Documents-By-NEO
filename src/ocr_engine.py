import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OCREngine:
    """Handles text extraction from cell images using Microsoft TrOCR."""
    
    def __init__(self, model_name="microsoft/trocr-base-printed"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Initializing TrOCR on {self.device}...")
        
        self.processor = TrOCRProcessor.from_pretrained(model_name)
        self.model = VisionEncoderDecoderModel.from_pretrained(model_name).to(self.device)

    def extract_text(self, cell_image):
        """Extracts text and confidence from a cropped cell image."""
        if cell_image.size[0] == 0 or cell_image.size[1] == 0:
            return "", 0.0
            
        pixel_values = self.processor(images=cell_image, return_tensors="pt").pixel_values.to(self.device)
        
        # Generate text with confidence scores (approximation via logprobs if needed, 
        # but standard generate gives output IDs)
        generated_ids = self.model.generate(pixel_values, return_dict_in_generate=True, output_scores=True)
        generated_text = self.processor.batch_decode(generated_ids.sequences, skip_special_tokens=True)[0]
        
        # Calculating a simple confidence score based on transition probabilities
        logits = torch.stack(generated_ids.scores, dim=1)
        probs = torch.softmax(logits, dim=-1)
        token_probs, _ = torch.max(probs, dim=-1)
        confidence = torch.mean(token_probs).item()
        
        return generated_text.strip(), confidence

if __name__ == "__main__":
    # Smoke test with a blank image
    engine = OCREngine()
    dummy_cell = Image.new('RGB', (100, 30), color='white')
    text, conf = engine.extract_text(dummy_cell)
    print(f"TrOCR Smoke Test: '{text}' (Confidence: {conf:.4f})")