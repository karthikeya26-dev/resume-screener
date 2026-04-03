import re

def calculate_ats_score(resume_text, job_description, extracted_skills):
    text_lower = resume_text.lower()
    jd_lower = job_description.lower()
    
    # 1. Sections (40%)
    sections_score = 0
    if re.search(r'\b(education|university|college|degree)\b', text_lower):
        sections_score += 15
    if re.search(r'\b(skills|technologies|tools)\b', text_lower) or len(extracted_skills) > 0:
        sections_score += 15
    if re.search(r'\b(projects|portfolio)\b', text_lower):
        sections_score += 10
        
    # 2. Keyword Matching (30%)
    jd_words = set(re.findall(r'\b[a-z]{4,}\b', jd_lower)) - {"with", "this", "that", "have", "from", "your", "what", "when", "where", "they"}
    match_count = sum(1 for word in jd_words if word in text_lower)
    keyword_score = 0
    if len(jd_words) > 0:
        keyword_score = min(30, int((match_count / len(jd_words)) * 30))
        
    # 3. Formatting (20%)
    length = len(resume_text)
    formatting_score = 0
    if 500 < length < 5000:
        formatting_score = 20
    elif length > 0:
        formatting_score = 10
        
    # 4. Experience Relevance (10%)
    experience_score = 0
    if re.search(r'\b(experience|work|employment|history)\b', text_lower):
        experience_score += 5
    if re.search(r'\b(years|months)\b', text_lower):
        experience_score += 5
        
    total_score = sections_score + keyword_score + formatting_score + experience_score
    
    return {
        "score": total_score,
        "details": {
            "sections": sections_score,
            "keywords": keyword_score,
            "formatting": formatting_score,
            "experience": experience_score
        }
    }
