from fpdf import FPDF
import os
from datetime import datetime

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'AI Data Analysis Executive Summary', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_summary(text: str, filename: str = "summary.pdf") -> str:
    """
    Generates a PDF summary report from the Agent's insights.
    Returns the file path.
    """
    # Fix the ascii issue by encoding to utf-8 if needed, fpdf2 handles unicode mostly
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    # Simple line breaks processing
    for line in text.split('\n'):
        # using multi_cell to handle line breaks and long lines
        pdf.multi_cell(0, 8, txt=line)
        
    export_dir = "/app/data/exports" if os.environ.get("PYTHONUNBUFFERED") else "data/exports"
    os.makedirs(export_dir, exist_ok=True)
    filepath = os.path.join(export_dir, f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}")
    
    pdf.output(filepath)
    return filepath
