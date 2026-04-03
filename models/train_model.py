import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import os
import sys
from sqlalchemy import text

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import MODEL_PATH, VECTORIZER_PATH, BASE_DIR
from database.db import engine

def seed_training_data_if_empty():
    """Migrates CSV to SQL exactly once if the table is empty"""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM training_data"))
        count = result.scalar()
        if count == 0:
            print("Training table is empty. Seeding from sample_dataset.csv...")
            data_path = os.path.join(BASE_DIR, "data", "sample_dataset.csv")
            try:
                df = pd.read_csv(data_path)
                df.to_sql('training_data', con=engine, if_exists='append', index=False)
                print(f"Successfully seeded {len(df)} rows into training_data table.")
            except Exception as e:
                print(f"Failed to seed database: {e}")

def train():
    try:
        # First, ensure data exists in table
        seed_training_data_if_empty()
        
        # Read from MySQL database instead of CSV
        df = pd.read_sql("SELECT text, role FROM training_data", con=engine)
        
        if df.empty:
            print("Error: No training data found in database.")
            return

        # Text data
        X = df["text"]
        y = df["role"]
        
        # Vectorization
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        X_vec = vectorizer.fit_transform(X)
        
        # Train test split
        X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)
        
        # Train
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)
        
        # Predict and evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print("Model Accuracy:", accuracy)
        
        # Save model and vectorizer
        with open(MODEL_PATH, "wb") as f:
            pickle.dump(model, f)
        with open(VECTORIZER_PATH, "wb") as f:
            pickle.dump(vectorizer, f)
            
        print(f"Model saved to {MODEL_PATH}")
        print(f"Vectorizer saved to {VECTORIZER_PATH}")
        
    except Exception as e:
        print(f"Training failed. Make sure your MySQL connection is correct in config.py. Error: {e}")

if __name__ == "__main__":
    train()
