from flask import Flask, render_template, request, jsonify
import spacy
import nltk
from nltk.stem import SnowballStemmer
import pandas as pd

# Downloading necessary models and resources
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading en_core_web_sm model...")
    nlp = spacy.load("en_core_web_sm")

try:
    stemmer = SnowballStemmer("english")
except LookupError:
    print("Downloading necessary NLTK data...")
    nltk.download('punkt')
    nltk.download('snowball_data')
    stemmer = SnowballStemmer("english")


class WebDataTokenizer:
    def __init__(self):
        self.stemmer = SnowballStemmer("english")

    def spacy_tokenize(self, text):
        doc = nlp(text)
        tokens = [token.text for token in doc if token.is_alpha]
        return tokens

    def apply_stemming(self, tokens):
        return [self.stemmer.stem(token) for token in tokens]

    def process_text(self, text):
        tokens = self.spacy_tokenize(text)
        stemmed_tokens = self.apply_stemming(tokens)
        return tokens, stemmed_tokens


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process_text', methods=['POST'])
def process_text():
    text = request.form['text']  # Taking text input from the form
    
    tokenizer = WebDataTokenizer()
    tokens, stemmed_tokens = tokenizer.process_text(text)
    
    # Prepare the result data
    df = pd.DataFrame({'Tokenization': tokens, 'Stemming': stemmed_tokens})
    result = df.to_dict(orient="records")  # Convert to list of dictionaries
    
    return jsonify({"Results": result})

if __name__ == "__main__":
    app.run(debug=True)
