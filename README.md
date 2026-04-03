# Smart Resume Screening & Job Matching System

## Prerequisites

1. Ensure you have Python 3.9+ installed.
2. Install a MySQL Database Server and have it running (optional, system gracefully falls back to SQLite automatically if MySQL connection fails).
3. (Optional) If you plan on extracting text from images, you need to install [Tesseract-OCR](https://github.com/tesseract-ocr/tesseract) on your system.

## Setup Instructions

1. Navigate to the project folder:
   ```bash
   cd C:\Users\karth\.gemini\antigravity\scratch\resume_screener
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure MySQL (If using MySQL instead of default SQLite):
   Open `config.py` and modify `DATABASE_URL` to match your MySQL credentials.
   Default: `mysql+pymysql://root:password@localhost/resume_db`
   *Make sure you create the `resume_db` schema in your MySQL server before running the app.*

## Running the Application

1. Start the web application:
   ```bash
   streamlit run app.py
   ```

2. **First Run Setup:**
   When the app opens in your browser, go to the **sidebar on the left** and click **Train ML Model**. This will generate the `model.pkl` and `vectorizer.pkl` files from the sample dataset.

3. **Candidate Mode:** 
   Upload your resume, paste a Job Description, and get your ATS Score, Role Prediction, and Improvement Roadmap (can be downloaded as a PDF).

4. **HR Mode:** 
   Upload multiple candidate resumes concurrently, paste the target Job Description, and the system stores them in the database and ranks them using our custom Matching Algorithm Formula!
