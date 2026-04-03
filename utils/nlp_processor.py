import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Setup NLTK resources gracefully
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s.,]', ' ', text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered = [w for w in tokens if not w in stop_words]
    return " ".join(filtered)

def extract_email(text):
    email = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return email.group(0) if email else "Not Found"

def extract_phone(text):
    phone = re.search(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', text)
    return phone.group(0) if phone else "Not Found"

def extract_skills(text, predefined_skills=None):
    if predefined_skills == None:
        predefined_skills = ["python", "java", "sql", "machine learning", "docker", "kubernetes", "react", "node.js", "django", "aws", "data analysis", "nlp", "html", "css", "javascript", "c++", "c#", "azure"]
    
    text_lower = text.lower()
    found_skills = []
    for skill in predefined_skills:
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found_skills.append(skill)
    return found_skills
