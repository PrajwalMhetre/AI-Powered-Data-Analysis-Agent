import pandas as pd
from typing import Optional
from core.security import sanitize_dataframe

class DataProcessor:
    @staticmethod
    def process_file(file_path: str) -> Optional[pd.DataFrame]:
        """
        Reads CSV or Excel file safely, dropping nulls and sanitizing 
        PII data for industrial standards.
        """
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("Unsupported file format")
                
            # Basic sanitization and cleanup
            df = df.dropna(how='all') # Drop fully empty rows
            
            # Anonymize data (Security feature)
            df = sanitize_dataframe(df)
            
            return df
        except Exception as e:
            raise Exception(f"Failed to process file: {str(e)}")
