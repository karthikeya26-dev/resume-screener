import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.extractor import extract_text
from utils.nlp_processor import extract_email, extract_skills
from utils.ats import calculate_ats_score
from utils.matcher import calculate_jd_match
from utils.skill_gap import analyze_skill_gap
from utils.report import generate_report
from models.predictor import predict_job_role
from database.db import get_db
from database.models import Candidate

def process_candidate_resume(file_path, filename, jd_text):
    text = extract_text(file_path)
    email = extract_email(text)
    skills = extract_skills(text)
    
    name = filename.split('.')[0] 
    
    pred_role, conf = predict_job_role(text)
    ats = calculate_ats_score(text, jd_text, skills)
    match_res = calculate_jd_match(text, jd_text)
    gap_res = analyze_skill_gap(skills, jd_text)
    
    report_path = generate_report(
        candidate_name=name,
        ats_score=ats["score"],
        match_percentage=match_res["match_percentage"],
        missing_skills=gap_res["missing_skills"],
        roadmap=gap_res["roadmap"]
    )
    
    db = next(get_db())
    candidate = Candidate(
        name=name,
        email=email,
        skills=", ".join(skills),
        predicted_role=pred_role,
        ats_score=ats["score"],
        jd_match=match_res["match_percentage"],
        missing_skills=", ".join(gap_res["missing_skills"]),
        resume_path=file_path
    )
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    
    return {
        "text": text,
        "email": email,
        "skills": skills,
        "predicted_role": pred_role,
        "ats": ats,
        "match": match_res,
        "gap": gap_res,
        "report_path": report_path
    }
