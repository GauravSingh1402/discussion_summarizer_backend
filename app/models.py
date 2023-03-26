import torch
from flask import Flask, jsonify, request
import requests
import time
import openai
import numpy as np
import json
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from string import punctuation
from collections import defaultdict
from heapq import nlargest
from transformers import T5ForConditionalGeneration, T5Tokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter
from transformers import BartForConditionalGeneration, BartTokenizer, AdamW
from transformers import AutoTokenizer, T5ForConditionalGeneration
API_URL = "https://api-inference.huggingface.co/models/Hridayesh7/autotrain-summasense-3584196302"


bart_tokenizer = BartTokenizer.from_pretrained("./model/bart/tokenizer")
bart_model = BartForConditionalGeneration.from_pretrained("./model/bart/model")
title_tokenizer = AutoTokenizer.from_pretrained("./model/title/tokenizer")
title_model = T5ForConditionalGeneration.from_pretrained("./model/title/model")
conversation_tokenizer = BartTokenizer.from_pretrained("./model/interview/tokenizer")
conversation_model = BartForConditionalGeneration.from_pretrained("./model/interview/model")

class SummarizerModel:

    def title(text):
        try:
            article = text
            inputs = title_tokenizer.encode(article, return_tensors='pt')
            title_ids = title_model.generate(inputs, max_length=50, num_beams=4, early_stopping=True)
            title = title_tokenizer.decode(title_ids.squeeze(), skip_special_tokens=True)
            return title
        except Exception as e:
            print(e)
            return "error"
        
        
    def bart(text):
        words = text.split()
        word_count=len(words)
        try:
            input_ids = bart_tokenizer(text, truncation=True, padding='longest', return_tensors='pt').input_ids
            summary_ids = bart_model.generate(input_ids,min_length=10, max_length=80, num_beams=4, early_stopping=True)
            summary = bart_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            summary_word=summary.split()
            summary_count=len(summary_word)
            summ = ', '.join(summary_word)
            return summary[:summary.rfind('.')+1]
        except Exception as e:
            print("Error:", e)
            return "error"
        
        
    def convo_bart(text):
        try:
            words = text.split()
            word_count=len(words)
            conversation=text
            inputs = conversation_tokenizer.encode(conversation, return_tensors='pt')
            summary_ids = conversation_model.generate(inputs, num_beams=4, max_length=200, early_stopping=True)
            summary = conversation_tokenizer.decode(summary_ids.squeeze(), skip_special_tokens=True)
            summary_word=summary.split()
            summary_count=len(summary_word)
            summ = ', '.join(summary_word)
            return summary[:summary.rfind('.')+1]
        except Exception as e:
            print("Error:", e)
            return "error"
        
        
        
    def lsa(text):
        try:
            words = text.split()
            word_count = len(words)
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
            svd_model = TruncatedSVD(n_components=1)
            svd_model.fit(vectorized_sentences)
            sentence_scores = vectorized_sentences.dot(svd_model.components_.T)
            threshold = np.mean(sentence_scores)
            summary = ''
            for i, sentence in enumerate(sentences):
                if sentence_scores[i] > threshold:
                    summary += sentence + ' '
            summary = summary.strip()
            summary_word = summary.split()
            summary_count = len(summary_word)
            summary_count=len(summary_word)
            print('LSA',summary)
            if summary_count<=word_count//2:
                return  summary
            else:
                    if len(summary) <= len(text) // 3:
                        return summary
                    else:
                        x=len(summary) // 3
                        summary=summary[:x+1]
                        summ = summary[:summary.rfind(".") + 1]
                        return  summ
        except Exception as e:
            print('lsa', e)
            return "error"


    def kl(text):
        words = text.split()
        word_count = len(words)
        try:
            stop_words = set(stopwords.words('english'))
            words = [word.lower() for word in word_tokenize(text) if word.isalnum() and word.lower() not in stop_words]
            word_freq = Counter(words)
            max_freq = max(word_freq.values())
            if max_freq > 0:
                for word in word_freq:
                    word_freq[word] /= max_freq
            summary = ''
            for sentence in sent_tokenize(text):
                sentence_words = [word.lower() for word in word_tokenize(sentence) if word.isalnum()]
                sentence_freq = Counter(sentence_words)
                # Compute KL divergence only for words in both the text and the sentence
                common_words = set(word_freq.keys()) & set(sentence_freq.keys())
                if common_words:
                    sentence_kl_div = sum(word_freq[i] * np.log2(word_freq[i] / sentence_freq[i]) for i in common_words)
                else:
                    sentence_kl_div = float('inf')
                # Compare KL divergence of sentence with previous sentence(s)
                common_words = set(word_freq.keys()) & set(sentence_freq.keys())
                new_sentence_score = sum(word_freq[i] * np.log2(word_freq[i] / sentence_freq[i]) for i in common_words)
                if new_sentence_score > sentence_kl_div:
                    summary = sentence
                summary = summary.strip() + ' ' + sentence
            if len(summary) <= len(text) // 3:
                return summary
            else:
                x=len(summary) // 3
                summary=summary[:x+1]
                summ = summary[:summary.rfind(".") + 1]
                return summ
        except Exception as e:
            print('kl', e)
            return 'error'

        
 

