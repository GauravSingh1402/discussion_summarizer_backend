from app import routes
from flask_cors import CORS
from flask_pymongo import pymongo
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, \
    unset_jwt_cookies, jwt_required, JWTManager
import redis
from app import config
app = Flask(__name__)
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "redis"
# app.config['SESSION_USE_SIGNER'] = True
# app.config['SESSION_REDIS'] = redis.from_url('redis://127.0.0.1:6379')
# app.config['SECRET_KEY'] = config.Config.SECRET_KEY
app.config['JWT_SECRET'] = config.Config.JWT_SECRET
app.config["JWT_ALGORITHM"] = "HS256"
jwt = JWTManager(app)
Session(app)
conn_string = config.Config.DATABASE_URI
mongoDB_client = pymongo.MongoClient(conn_string)
db = mongoDB_client.get_database('summarizer')
CORS(app)
cors = CORS(app, resource={
    r"/*": {
        "origins": "*"
    }
})
