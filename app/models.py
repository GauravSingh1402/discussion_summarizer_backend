import torch
from flask import Flask, jsonify, request
import requests
import time
import openai
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import random
import sys

from keras.callbacks import LambdaCallback
from keras.models import Sequential
from keras.layers import Dense, LSTM


API_URL = "https://api-inference.huggingface.co/models/Hridayesh7/autotrain-summasense-3584196302"



class SummarizerModel:


    def title_generator(text):
        chars = sorted(list(set(text)))
        char_indices = dict((c, i) for i, c in enumerate(chars))
        indices_char = dict((i, c) for i, c in enumerate(chars))

        # Cut the text into subsequences of a fixed length
        maxlen = 40
        step = 3
        sentences = []
        next_chars = []
        for i in range(0, len(text) - maxlen, step):
            sentences.append(text[i : i + maxlen])
            next_chars.append(text[i + maxlen])
            
        # Vectorize the sentences and next_chars
        x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
        y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
        for i, sentence in enumerate(sentences):
            for t, char in enumerate(sentence):
                x[i, t, char_indices[char]] = 1
            y[i, char_indices[next_chars[i]]] = 1
        model = Sequential()
        model.add(LSTM(128, input_shape=(maxlen, len(chars))))
        model.add(Dense(len(chars), activation="softmax"))

        # Compile the model
        model.compile(loss="categorical_crossentropy", optimizer="adam")

        # Define a function to sample a character from the model's output distribution
        def sample(preds, temperature=1.0):
            preds = np.asarray(preds).astype("float64")
            preds = np.log(preds) / temperature
            exp_preds = np.exp(preds)
            preds = exp_preds / np.sum(exp_preds)
            probas = np.random.multinomial(1, preds, 1)
            return np.argmax(probas)

        
    def gpt(text):
        try:
            openai.api_key = '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'
            model_engine = "text-davinci-002"
            prompt_prefix = "Please summarize the following text:"
            temperature = 0.7
            max_tokens = 200
            prompt = prompt_prefix + "\n" + text
            response = openai.Completion.create(engine=model_engine, prompt=prompt, temperature=temperature, max_tokens=max_tokens)
            summary = response.choices[0].text.strip()
            return summary
        except Exception as e:
            print("H",e)
            return "error"

        
    def lsa(text,num_sent):
        try:
            stop_words = set(stopwords.words('english'))
            wordnet_lemmatizer = WordNetLemmatizer()
            sentences = nltk.sent_tokenize(text)
            clean_sentences = []
            for sentence in sentences:
                words = nltk.word_tokenize(sentence)
                words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
                words = [wordnet_lemmatizer.lemmatize(word) for word in words]
                clean_sentences.append(' '.join(words))
            vectorizer = TfidfVectorizer()
            vectorized_sentences = vectorizer.fit_transform(clean_sentences)
            lsa_model = TruncatedSVD(n_components=1)
            lsa_model.fit(vectorized_sentences)
            sentence_scores = vectorized_sentences.dot(lsa_model.components_.T)
            top_sentence_indices = np.argsort(sentence_scores.flatten())[::-1][:num_sent]
            top_sentence_indices.sort()
            summary = ' '.join([sentences[i] for i in top_sentence_indices])
            return summary
        except Exception as e:
            print(e)
            return "error"


    def kl(text,n_sentences):
        print(n_sentences)
        if n_sentences is None:
            n_sentences = 5
        try:
            stop_words = set(stopwords.words('english'))
            words = [word.lower() for word in word_tokenize(text) if word.isalnum() and word.lower() not in stop_words]
            word_freq = Counter(words)
            max_freq = max(word_freq.values())

            if max_freq > 0:
                for word in word_freq:
                    word_freq[word] /= max_freq

            summary = ''
            for i, sentence in enumerate(sent_tokenize(text)):
                sentence_words = [word.lower() for word in word_tokenize(sentence) if word.isalnum()]
                sentence_freq = Counter(sentence_words)
                # Compute KL divergence only for words in both the text and the sentence
                common_words = set(word_freq.keys()) & set(sentence_freq.keys())
                if common_words:
                    sentence_kl_div = sum(word_freq[i] * np.log2(word_freq[i] / sentence_freq[i]) for i in common_words)
                else:
                    sentence_kl_div = float('inf')
                if i < n_sentences:
                    summary += sentence + ' '
                else:
                    # Compute KL divergence for the whole text and the current sentence
                    common_words = set(word_freq.keys()) & set(sentence_freq.keys())
                    new_sentence_score = sum(word_freq[i] * np.log2(word_freq[i] / sentence_freq[i]) for i in common_words)
                    if new_sentence_score > sentence_kl_div:
                        summary = summary.replace(summary.split()[-1], sentence, 1)
            summary = summary.strip()
            return summary
        except Exception as e:
            print(e)
            return 'error'

