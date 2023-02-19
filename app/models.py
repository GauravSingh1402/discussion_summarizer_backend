import torch
from flask import Flask, jsonify, request
import requests
from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import BartForConditionalGeneration, BartTokenizer, BartConfig
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.kl import KLSummarizer
import time
# from gensim.summarization import summarize

# bart_tokenizer=BartTokenizer.from_pretrained('facebook/bart-large-cnn')
# bart_model=BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
import requests


API_URL = "https://api-inference.huggingface.co/models/Hridayesh7/autotrain-summasense-3584196302"


class SummarizerModel:
    def t5_summarizer(text,stop_words,top):
        try:
            while True:
                loading_response = requests.get(API_URL)
                if loading_response.json()["model_status"]["ready"]:
                    break
                time.sleep(loading_response.json()["model_status"]["estimated_time"])
            headers = {"Authorization": "Bearer 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"}
            data = {
                "inputs": f"summarize: {text}",
                 "parameters": {
                    "do_sample": True,
                    "max_length": stop_words,
                    "top_k": top,
                    "num_return_sequences": 1,
                    },
                }
            response = requests.post(API_URL, headers=headers, json=data)
            print("Yup",response.json())
            summary = response.json()[0]['summary_text']
            return summary
        except Exception as e:
            print(e)
            return "error"
        
    def lsa(text,stop_words):
        try:
            parser=PlaintextParser.from_string(text,Tokenizer('english'))
            lsa_summarizer=LsaSummarizer()
            lsa_summary= str(list(lsa_summarizer(parser.document,stop_words)))
            lsa_summary = lsa_summary[11:]
            lsa_summary = lsa_summary[:-1]
            return lsa_summary
        except Exception as e:
            print(e)
            return "error"

    def kl(text,stop_words):
        try:
            parser=PlaintextParser.from_string(text,Tokenizer('english'))
            kl_summarizer=KLSummarizer()
            kl_summary=str(list(kl_summarizer(parser.document,stop_words)))
            kl_summary = kl_summary[11:]
            kl_summary = kl_summary[:-1]
            return kl_summary
        except Exception as e:
            print(e)
            return "error"
        