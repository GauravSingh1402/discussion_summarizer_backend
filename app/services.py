from flask import jsonify, request
from app import app
import re
import string
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import numpy as np

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
    def preprocess_text(text):
        stop_words = set(stopwords.words('english'))
        words = [word.lower() for word in word_tokenize(text) if word.isalnum() and word.lower() not in stop_words]
        word_freq = Counter(words)
        max_freq = max(word_freq.values())
        if max_freq > 0:
            for word in word_freq:
                word_freq[word] /= max_freq
        return word_freq
    def kl_divergence(p, q):
        return sum(p[i] * np.log2(p[i] / q[i]) for i in p)