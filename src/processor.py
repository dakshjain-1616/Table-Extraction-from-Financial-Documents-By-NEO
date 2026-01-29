import pandas as pd
import numpy as np
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TableProcessor:
    """Processes OCR results into structured DataFrames with financial normalization."""
    
    def __init__(self):
        pass

    def reconstruct_table(self, cells):
        """
        Reconstructs a table from cell data.
        cells: list of dicts with {'text': str, 'conf': float, 'row': int, 'col': int}
        """
        if not cells:
            return pd.DataFrame()
            
        df = pd.DataFrame(cells)
        # Handle cases where multiple segments fall into same row/col (merges/multi-line)
        pivot_df = df.pivot_table(
            index='row', 
            columns='col', 
            values='text', 
            aggfunc=lambda x: ' '.join(str(v) for v in x if v)
        ).fillna('')
        
        return pivot_df

    def normalize_financial_text(self, text):
        """Cleans and normalizes financial strings."""
        if not text:
            return "0.00"
            
        # Remove currency symbols but keep decimal/minus
        cleaned = re.sub(r'[^\d\.\-]', '', text)
        
        # Handle empty or just symbols
        if not cleaned or cleaned == '.' or cleaned == '-':
            return text
            
        try:
            val = float(cleaned)
            return f"{val:.2f}"
        except ValueError:
            return text

    def process_table(self, raw_table_data):
        """
        raw_table_data: list of cells with inferred row/col indices.
        """
        df = self.reconstruct_table(raw_table_data)
        
        # Apply normalization to potential financial columns (heuristic: columns with lots of digits)
        for col in df.columns:
            digit_ratio = df[col].apply(lambda x: len(re.findall(r'\d', str(x))) / (len(str(x)) + 1)).mean()
            if digit_ratio > 0.4:
                df[col] = df[col].apply(self.normalize_financial_text)
                
        return df

if __name__ == "__main__":
    # Smoke test
    cells = [
        {'text': 'Date', 'row': 0, 'col': 0, 'conf': 0.9},
        {'text': 'Amount', 'row': 0, 'col': 1, 'conf': 0.9},
        {'text': '2023-01-01', 'row': 1, 'col': 0, 'conf': 0.8},
        {'text': '$ 1,234.56', 'row': 1, 'col': 1, 'conf': 0.85},
    ]
    processor = TableProcessor()
    df = processor.process_table(cells)
    print("Processed Table:")
    print(df)