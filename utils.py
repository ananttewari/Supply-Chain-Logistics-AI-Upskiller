import os
import streamlit as st

def load_config():
    """
    Load configuration from Streamlit secrets or environment variables.
    """
    try:
        return st.secrets
    except FileNotFoundError:
        return {}

def get_directories():
    """
    Return the list of data directories.
    """
    return [
        "Job Descriptions",
        "Industry Reports",
        "Training Curricula"
    ]

def ensure_directory_exists(path):
    """
    Ensure that a directory exists.
    """
    if not os.path.exists(path):
        os.makedirs(path)

# NEW: PDF Report Generator
def generate_pdf_report(role, literacy_level, quiz_score, roadmap_text=None):
    """
    Generates a PDF report for the user.
    Returns bytes content of the PDF.
    """
    try:
        from fpdf import FPDF
    except ImportError:
        return None

    class ReportPDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 15)
            self.cell(0, 10, 'Semiconductor Logistics AI-Upskiller | Career Report', 0, 1, 'C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    pdf = ReportPDF()
    pdf.add_page()
    
    # 1. Profile Summary
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "1. Professional Profile", 0, 1)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 10, f"Target Role: {role}", 0, 1)
    pdf.cell(0, 10, f"Current AI Literacy Level: {literacy_level}/5", 0, 1)
    
    # 2. Competency Gap Analysis (Simulated based on Role logic)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "2. Competency Gap Analysis", 0, 1)
    pdf.set_font("Arial", '', 11)
    
    # Replicate the logic from main.py
    base_val = literacy_level
    if role == "Logistics Manager":
        skills = {"Logistics Ops": base_val+1, "Procurement": base_val-1}
    elif role == "Supply Chain Analyst":
        skills = {"Data Literacy": base_val+2, "AI Strategy": base_val+1}
    else:
        skills = {"General Operations": base_val}
        
    for skill, val in skills.items():
        pdf.cell(0, 7, f"- {skill}: Level {min(val, 5)}/5", 0, 1)
        
    # 3. Assessment Results
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "3. Quiz Performance", 0, 1)
    pdf.set_font("Arial", '', 11)
    if quiz_score is not None:
        pdf.cell(0, 10, f"Make-A-Quiz Score: {quiz_score}/5", 0, 1)
    else:
        pdf.cell(0, 10, "No quiz attempted yet.", 0, 1)
        
    # 4. Roadmap Summary
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "4. Recommended Action Plan", 0, 1)
    pdf.set_font("Arial", '', 11)
    if roadmap_text:
        # Simple cleanup to remove markdown bolding for PDF
        clean_text = roadmap_text.replace('**', '').replace('###', '')
        # Multi-cell for wrapping text
        pdf.multi_cell(0, 6, clean_text[:2000] + ("..." if len(clean_text) > 2000 else ""))
    else:
        pdf.cell(0, 10, "Please generate a roadmap in the 'Learning Path' tab to see it here.", 0, 1)

    return pdf.output(dest='S').encode('latin-1', 'replace')
