import os
import logging
from PIL import Image
import numpy as np

# Use try-except for robust loading
try:
    from pdf2image import convert_from_path
except ImportError:
    convert_from_path = None

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DocumentLoader:
    """Handles loading and normalization of PDF and Image documents."""
    
    def __init__(self, output_resolution=300):
        self.output_resolution = output_resolution

    def load(self, file_path):
        """Loads a document and returns a list of PIL Images."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            if convert_from_path is None:
                raise ImportError("pdf2image not installed correctly. Cannot process PDFs.")
            return self._load_pdf(file_path)
        elif ext in ['.jpg', '.jpeg', '.png', '.tiff', '.bmp']:
            return [self._load_image(file_path)]
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def _load_pdf(self, pdf_path):
        logger.info(f"Converting PDF to images: {pdf_path}")
        try:
            images = convert_from_path(pdf_path, dpi=self.output_resolution)
            return images
        except Exception as e:
            logger.error(f"Failed to convert PDF: {e}")
            raise

    def _load_image(self, image_path):
        logger.info(f"Loading image: {image_path}")
        return Image.open(image_path).convert("RGB")

if __name__ == "__main__":
    # Use relative paths for local testing
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_data_dir = os.path.join(base_dir, "data", "raw")
    os.makedirs(raw_data_dir, exist_ok=True)
    
    # Create test image
    test_img_path = os.path.join(raw_data_dir, "test_image.png")
    Image.new('RGB', (100, 100), color='white').save(test_img_path)
    
    loader = DocumentLoader()
    images = loader.load(test_img_path)
    print(f"Loaded {len(images)} images.")
    print(f"Image properties: {images[0].size}, {images[0].mode}")