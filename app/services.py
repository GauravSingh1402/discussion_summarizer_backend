from flask import jsonify, request
from app import app
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter
import numpy as np

class Service:
    def listen(text):
        try:
            text = re.sub(r'\b(um|uh|ah|like)\b', '', text)
            # Correct spelling and grammar errors
            # (Assuming you have a dictionary of known spelling errors and their corrections)
            # Remove irrelevant information
            text = re.sub(r'\b(inaudible|background noise|laughter)\b', '', text)
            # Standardize formatting
            text = text.replace('\n', ' ')
            text = re.sub(r'([.?!])\s+', r'\1 ', text)
            # Identify and remove duplicates
            sentences = text.split('. ')
            unique_sentences = list(set(sentences))
            # Segment the text into smaller chunks
            chunks = [unique_sentences[i:i+5] for i in range(0, len(unique_sentences), 5)]
            preprocessed_text = ''
            for chunk in chunks:
                preprocessed_text += '. '.join(chunk) + '.\n'
            return preprocessed_text
        except Exception as e:
            print('s',e)
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