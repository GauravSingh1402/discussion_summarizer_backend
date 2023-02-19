from flask import jsonify, request
from app import app
import re
import string
import nltk
from nltk.stem import WordNetLemmatizer
class Service:
    def listen(text):
        try:
            nltk.download('omw-1.4')
            nltk.download('stopwords')
            nltk.download('wordnet')
            nltk.download('punkt')
            lemmatizer = WordNetLemmatizer()
            clean_text = ' '.join([lemmatizer.lemmatize(word) for word in text.split() if word not in nltk.corpus.stopwords.words('english') and word not in string.punctuation])
            for k in clean_text.split("\n"):
                clean_text = re.sub(r"[^a-zA-Z0-9]+", ' ', k)
            return clean_text
        except Exception as e:
            print(e)
            return "error"
    