import streamlit as st
import os
import pandas as pd
from config import UPLOAD_FOLDER
from services.candidate_service import process_candidate_resume
from services.hr_service import rank_candidates
from models.train_model import train

st.set_page_config(page_title="Smart Resume System", layout="wide")

st.title("📄 Smart Resume Screening & Job Matching")

# Admin tools in sidebar
st.sidebar.header("Admin / Configuration")
if st.sidebar.button("Train ML Model (Run Once)"):
    with st.spinner("Training model on sample dataset..."):
        train()
        st.sidebar.success("Model trained successfully!")

# Tabs
tab1, tab2 = st.tabs(["👤 Candidate Mode", "👨‍💼 HR Mode"])

with tab1:
    st.header("Upload Your Resume for Scoring")
    resume_file = st.file_uploader("Upload Resume (PDF, DOCX, TXT, IMG)", type=["pdf", "docx", "txt", "png", "jpg", "jpeg"], key="candidate_resume")
    
    jd_input = st.text_area("Enter Job Description", height=200, key="candidate_jd")
    
    if st.button("Score My Resume"):
        if resume_file and jd_input:
            with st.spinner("Analyzing your resume..."):
                file_path = os.path.join(UPLOAD_FOLDER, resume_file.name)
                with open(file_path, "wb") as f:
                    f.write(resume_file.getbuffer())
                    
                result = process_candidate_resume(file_path, resume_file.name, jd_input)
                
                st.subheader("🎯 Results")
                col1, col2, col3 = st.columns(3)
                col1.metric("Predicted Role", result['predicted_role'])
                col2.metric("ATS Score", f"{result['ats']['score']} / 100")
                col3.metric("JD Match", f"{result['match']['match_percentage']} %")
                
                st.subheader("ATS Score Breakdown")
                st.json(result['ats']['details'])
                
                st.subheader("🔍 Skill Gap Analysis")
                st.write("**Missing Skills:**", ", ".join(result['gap']['missing_skills']) if result['gap']['missing_skills'] else "None. Great job!")
                st.write("**Your Roadmap:**")
                st.code(result['gap']['roadmap'])
                
                st.success("Analysis complete and saved to database!")
                
                # Download report
                if os.path.exists(result['report_path']):
                    with open(result['report_path'], "rb") as f:
                        st.download_button(
                            label="Download PDF Report",
                            data=f,
                            file_name=os.path.basename(result['report_path']),
                            mime="application/pdf"
                        )
        else:
            st.warning("Please upload a resume and enter a job description.")


with tab2:
    st.header("HR Dashboard - Bulk Rank Candidates")
    
    hr_resumes = st.file_uploader("Upload Multiple Resumes", type=["pdf", "docx", "txt", "png", "jpg", "jpeg"], accept_multiple_files=True, key="hr_resumes")
    hr_jd_input = st.text_area("Enter Job Description for Ranking", height=200, key="hr_jd")
    
    if st.button("Process & Rank Candidates"):
        if hr_resumes and hr_jd_input:
            with st.spinner(f"Processing {len(hr_resumes)} resumes..."):
                for rf in hr_resumes:
                    file_path = os.path.join(UPLOAD_FOLDER, rf.name)
                    with open(file_path, "wb") as f:
                        f.write(rf.getbuffer())
                    # Process and save to DB
                    process_candidate_resume(file_path, rf.name, hr_jd_input)
                
                # Retrieve ranking
                ranking = rank_candidates(hr_jd_input)
                df = pd.DataFrame(ranking)
                
                st.subheader("🏆 Ranked Candidates")
                st.dataframe(df.style.highlight_max(subset=['Final Ranking Score', 'JD Match %'], color='lightgreen'))
                
        elif hr_jd_input and not hr_resumes:
            st.info("No new resumes uploaded. Showing rankings of existing candidates in the database for this JD.")
            ranking = rank_candidates(hr_jd_input)
            df = pd.DataFrame(ranking)
            st.dataframe(df)
        else:
            st.warning("Please enter a job description.")
