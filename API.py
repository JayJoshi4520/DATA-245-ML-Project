from flask import Flask, request, jsonify
import joblib
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from flask_cors import CORS
import nltk
from nltk.corpus import stopwords

# Create Flask app
app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "http://localhost:3000"}})  # Enable CORS for all routes

# Load models
logistic_model = joblib.load('./model/logistic_regression_model.pkl')
naive_bayes_model = joblib.load('./model/naive_bayes_model.pkl')
svm_model = joblib.load('./model/svm_model.pkl')
lstm_model = tf.keras.models.load_model('./model/lstm_model.h5')
cnn_model = tf.keras.models.load_model('./model/cnn_model.h5')
tokenizer = joblib.load('./model/tokenizer.pkl')

# Preprocess text function
def preprocess_text(text):
    import re
    stop_words = set(stopwords.words('english'))
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

# Prediction endpoint
@app.route('/predict', methods=['POST'])
def predict():
    # Get the article from request
    data = request.get_json()
    article = data.get('article', '')

    # Preprocess the article
    preprocessed_article = preprocess_text(article)

    # Tokenize and pad the article for deep learning models
    seq = tokenizer.texts_to_sequences([preprocessed_article])
    pad_seq = pad_sequences(seq, maxlen=200)

    # Predict with each model
    logistic_prediction = logistic_model.predict([preprocessed_article])[0]
    naive_bayes_prediction = naive_bayes_model.predict([preprocessed_article])[0]
    svm_prediction = svm_model.predict([preprocessed_article])[0]
    lstm_prediction = lstm_model.predict(pad_seq)[0][0]
    cnn_prediction = cnn_model.predict(pad_seq)[0][0]

    # Prepare the response
    response = {
        'LogisticRegression': 'True News' if logistic_prediction == 1 else 'Fake News',
        'NaiveBayes': 'True News' if naive_bayes_prediction == 1 else 'Fake News',
        'SVM': 'True News' if svm_prediction == 1 else 'Fake News',
        'LSTM': 'True News' if lstm_prediction >= 0.5 else 'Fake News',
        'CNN': 'True News' if cnn_prediction >= 0.5 else 'Fake News'
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
