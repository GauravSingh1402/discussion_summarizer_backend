from flask_cors import CORS
from flask_pymongo import pymongo
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager
from flask_bcrypt import Bcrypt
import redis
from app import config

app=Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = config.Config.SECRET_KEY
app.config['JWT_SECRET_KEY'] = config.Config.JWT_SECRET_KEY

jwt = JWTManager(app)
Session(app)

conn_string = config.Config.DATABASE_URI
mongoDB_client = pymongo.MongoClient(conn_string)
db = mongoDB_client.get_database('summarizer')

CORS(app, resources={
    r'/*': {
        'origins': ['http://localhost:3000', 'https://summa-sense.vercel.app'],
        'supports_credentials': True,
        'allow_headers': ['Content-Type', 'Authorization'],
        'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    }
}, send_wildcard=False)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


from app import routes
