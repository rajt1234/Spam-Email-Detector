"""
Flask backend for the Spam Email Detection web app.
Serves the frontend and exposes a /predict API endpoint.
"""
import os
import joblib
from flask import Flask, request, jsonify, render_template

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'model')
MODEL_PATH = os.path.join(MODEL_DIR, 'model.pkl')
VECTORIZER_PATH = os.path.join(MODEL_DIR, 'vectorizer.pkl')

app = Flask(__name__)

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def predict_message(message):
    """Predict whether a message is Spam or Ham."""
    message_vector = vectorizer.transform([message])
    prediction = model.predict(message_vector)
    return 'Spam' if prediction[0] == 1 else 'Ham'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(silent=True) or {}
    message = data.get('message', '').strip()
    if not message:
        return jsonify({'error': 'Please provide a message to analyze.'}), 400
    result = predict_message(message)
    return jsonify({'prediction': result})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)