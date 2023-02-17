from flask_cors import CORS
from flask_pymongo import pymongo
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
import redis

app=Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "redis"
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.from_url('redis://127.0.0.1:6379')
app.config['SECRET_KEY'] = 'eb2879129ee008af7397c67e06a18f636560786d'
Session(app)
conn_string = "mongodb+srv://hridayesh:WN7WWkbBNk7viXB2@cluster0.hlqlkgj.mongodb.net/?retryWrites=true&w=majority"
mongoDB_client = pymongo.MongoClient(conn_string)
db = mongoDB_client.get_database('summarizer')
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})
from app import routes