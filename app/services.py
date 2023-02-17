from flask import jsonify, request
from app import app
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
            print(text)
            clean_text = ' '.join([lemmatizer.lemmatize(word) for word in text.split() if word not in nltk.corpus.stopwords.words('english') and word not in string.punctuation])
            clean_text = ''.join(e for e in clean_text if e.isalnum())
            print(clean_text)
            return clean_text
        except Exception as e:
            print(e)
            return "error"
    