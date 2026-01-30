import torch
from transformers import TrOCRProcessor, VisionEncoderDecoderModel, logging as transformers_logging
from PIL import Image
import logging
import warnings

# Use error level for transformers
transformers_logging.set_verbosity_error()

logger = logging.getLogger(__name__)
# Inherit settings but explicitly set this component to INFO if needed for its own logs
logger.setLevel(logging.INFO)

class OCREngine:
    """Handles text extraction from cell images using Microsoft TrOCR."""
    
    def __init__(self, model_name="microsoft/trocr-base-printed"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Initializing TrOCR on {self.device}...")
        
        self.processor = TrOCRProcessor.from_pretrained(model_name)
        self.model = VisionEncoderDecoderModel.from_pretrained(model_name).to(self.device)

    def extract_text(self, cell_image, num_beams=5):
        """
        Extracts text and confidence from a cropped cell image using optimized beam search.
        """
        if cell_image.size[0] == 0 or cell_image.size[1] == 0:
            return "", 0.0
            
        pixel_values = self.processor(images=cell_image, return_tensors="pt").pixel_values.to(self.device)
        
        # Optimized generation with Beam Search
        generated_ids = self.model.generate(
            pixel_values, 
            return_dict_in_generate=True, 
            output_scores=True,
            num_beams=num_beams,
            early_stopping=True,
            max_new_tokens=64
        )
        
        generated_text = self.processor.batch_decode(generated_ids.sequences, skip_special_tokens=True)[0]
        
        # Calculating confidence score using sequence transition probabilities
        # TrOCR sequences include the initial start token, so we align scores accordingly
        logits = torch.stack(generated_ids.scores, dim=1)  # [batch, seq_len, vocab]
        probs = torch.softmax(logits, dim=-1)
        
        # Map the generated IDs (excluding start token) to their probabilities
        # sequence format: [SOS, ID1, ID2, ..., EOS]
        seq_ids = generated_ids.sequences[0, 1:] 
        
        confidences = []
        for i, token_id in enumerate(seq_ids):
            if i < probs.size(1):
                confidences.append(probs[0, i, token_id].item())
        
        confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        return generated_text.strip(), confidence

if __name__ == "__main__":
    # Smoke test with a blank image
    engine = OCREngine()
    dummy_cell = Image.new('RGB', (100, 30), color='white')
    text, conf = engine.extract_text(dummy_cell)
    print(f"TrOCR Smoke Test: '{text}' (Confidence: {conf:.4f})")