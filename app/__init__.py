from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
app=Flask(__name__)
app.config['SECRET_KEY'] = 'eb2879129ee008af7397c67e06a18f636560786d'
app.config['MONGO_URI'] = "mongodb+srv://hridayesh:9sJXz4lEi2jMLjxg@cluster0.hlqlkgj.mongodb.net/?retryWrites=true&w=majority"
mongoDB_client = PyMongo(app)
db = mongoDB_client.db
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})
from app import routes