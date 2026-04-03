from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BASE_DIR

def generate_report(candidate_name, ats_score, match_percentage, missing_skills, roadmap):
    reports_dir = os.path.join(BASE_DIR, "static", "reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    filename = f"{candidate_name.replace(' ', '_')}_report.pdf"
    filepath = os.path.join(reports_dir, filename)
    
    c = canvas.Canvas(filepath, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, f"ATS & Job Match Report - {candidate_name}")
    
    c.setFont("Helvetica", 12)
    c.drawString(50, 710, f"ATS Score: {ats_score}/100")
    c.drawString(50, 690, f"JD Match: {match_percentage}%")
    
    c.drawString(50, 650, "Missing Skills:")
    skills_text = ", ".join(missing_skills) if missing_skills else "None"
    c.drawString(70, 630, skills_text)
    
    c.drawString(50, 590, "Improvement Roadmap:")
    y_pos = 570
    for line in roadmap.split("\n"):
        c.drawString(70, y_pos, line)
        y_pos -= 20
        
    c.save()
    return filepath
