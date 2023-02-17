from flask import Flask
from flask_cors import CORS
from flask_pymongo import pymongo
app=Flask(__name__)
app.config['SECRET_KEY'] = 'eb2879129ee008af7397c67e06a18f636560786d'
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