from flask_cors import CORS
from flask_pymongo import pymongo
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity,  unset_jwt_cookies, jwt_required, JWTManager
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
import redis
from app import config
import os

app=Flask(__name__)
bcrypt = Bcrypt(app)


app.config['SECRET_KEY'] = config.Config.SECRET_KEY
app.config['JWT_SECRET_KEY'] = config.Config.JWT_SECRET_KEY
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD')

jwt = JWTManager(app)
mail=Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
Session(app)

conn_string = config.Config.DATABASE_URI
mongoDB_client = pymongo.MongoClient(conn_string)
db = mongoDB_client.get_database('summarizer')
CORS(app, resources={
    r'/*': {
        'origins': ['https://summa-sense.vercel.app','http://localhost:3000'],
        'allow_headers': ['Content-Type', 'Authorization'],
        'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
        'supports_credentials': True,
        'allow_credentials': True
    }
}, send_wildcard=False)






from app import routes
