import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db import get_db
from database.models import Candidate

def rank_candidates(jd_text):
    db = next(get_db())
    candidates = db.query(Candidate).all()
    
    ranked = []
    for c in candidates:
        jd_match_val = c.jd_match if c.jd_match else 0.0
        ats_val = c.ats_score if c.ats_score else 0.0
        role_conf = 80.0 
        
        final_score = (0.5 * jd_match_val) + (0.3 * ats_val) + (0.2 * role_conf)
        
        ranked.append({
            "Name": c.name,
            "Predicted Role": c.predicted_role,
            "Skills": c.skills,
            "JD Match %": jd_match_val,
            "ATS Score": ats_val,
            "Final Ranking Score": round(final_score, 2),
            "ID": c.id
        })
        
    ranked = sorted(ranked, key=lambda x: x["Final Ranking Score"], reverse=True)
    return ranked
