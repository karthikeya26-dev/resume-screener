import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Default to local MySQL, but allow Render to override via Environment Variables
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:Karthik%402026@localhost/resume_db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
MODEL_DIR = os.path.join(BASE_DIR, "models", "saved")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
