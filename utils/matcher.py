from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def calculate_jd_match(resume_text, jd_text):
    if not jd_text or not resume_text:
        return {"match_percentage": 0.0, "missing_keywords": []}
        
    # Cosine Similarity
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    except ValueError:
        similarity = 0.0
        
    match_percentage = round(similarity * 100, 2)
    
    # Missing Keywords
    jd_words = set(re.findall(r'\b[A-Za-z]{4,}\b', jd_text.lower()))
    resume_words = set(re.findall(r'\b[A-Za-z]{4,}\b', resume_text.lower()))
    
    missing_keywords = list(jd_words - resume_words)[:10] 
    
    return {
        "match_percentage": match_percentage,
        "missing_keywords": missing_keywords
    }
