"""
Train the Spam Email Detection model and persist it to disk.
Run this script once to generate model.pkl and vectorizer.pkl
"""
import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, '..', 'emails.csv')
MODEL_DIR = os.path.join(BASE_DIR, 'model')
MODEL_PATH = os.path.join(MODEL_DIR, 'model.pkl')
VECTORIZER_PATH = os.path.join(MODEL_DIR, 'vectorizer.pkl')

os.makedirs(MODEL_DIR, exist_ok=True)

# Load dataset
dataset = pd.read_csv(DATA_PATH)

# Vectorization
vectorizer = CountVectorizer()
x = vectorizer.fit_transform(dataset['text'])
y = dataset['spam']

# Split data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Train model
model = MultinomialNB()
model.fit(x_train, y_train)

# Evaluate
y_pred = model.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy:.4f}")

# Persist artifacts
joblib.dump(model, MODEL_PATH)
joblib.dump(vectorizer, VECTORIZER_PATH)
print(f"Model saved to: {MODEL_PATH}")
print(f"Vectorizer saved to: {VECTORIZER_PATH}")