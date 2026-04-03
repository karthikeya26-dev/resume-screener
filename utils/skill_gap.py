def analyze_skill_gap(candidate_skills, jd_text):
    jd_lower = jd_text.lower()
    common_skills = ["sql", "python", "java", "machine learning", "docker", "react", "kubernetes", "aws", "nlp", "javascript", "c++", "azure", "c#", "django"]
    
    jd_skills = [skill for skill in common_skills if skill in jd_lower]
    
    missing_skills = [skill for skill in jd_skills if skill not in [cs.lower() for cs in candidate_skills]]
    
    roadmap = []
    if missing_skills:
        for ms in missing_skills:
            if ms == "sql":
                roadmap.append("- Learn SQL basics (joins, queries)")
            elif ms in ["machine learning", "nlp"]:
                roadmap.append(f"- Practice {ms} with scikit-learn or similar framework")
            else:
                roadmap.append(f"- Take a crash course on {ms}")
                
        roadmap.append("- Build 2 projects:")
        roadmap.append("   1. Sales prediction (or domain specific)")
        roadmap.append("   2. Resume classifier")
    else:
        roadmap.append("- You have matching skills! Focus on advanced interview prep.")
        
    return {
        "missing_skills": missing_skills,
        "roadmap": "\n".join(roadmap)
    }
