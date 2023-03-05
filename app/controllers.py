from flask import jsonify, request, session, Response
# from app import app
from app import db
from datetime import datetime
from flask_session import Session
import bcrypt
import os
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
import hashlib


class AudioController:
    def listen(x):
        return x
    
    def signup(x):
        try:
            if (x['email'] != '' or x['first_name'] != '' or x['last_name'] != ''):
                email = x['email']
                first_name = x['first_name']
                last_name = x['last_name']
                password=x['password']
                hashed_password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                result = db.user.find_one(
                    {"email": email, }, {'_id': 0, 'first_name': 1, 'last_name': 1})
                if not result:
                    db.user.insert_one({
                        "email": email,
                        "first_name": first_name,
                        "last_name": last_name,
                        "password": hashed_password,
                        "summary":[],
                        "created_date": datetime.utcnow()
                    })
                    return jsonify({"data" : "Inserted"}),200
                else:
                     return jsonify({"data" : "User Already Exists"})
            else:
                 return jsonify({"data" : "Fill all details"})
        except Exception as e:
            print(e)
            return "error"

    def gsignup(x):
        try:
            if (x['email'] != '' or x['first_name'] != '' or x['last_name'] != ''):
                email = x['email']
                first_name = x['first_name']
                last_name = x['last_name']
                print(email, first_name, last_name)
                result = db.user.find_one(
                    {"email": email, }, {'_id': 0, 'first_name': 1, 'last_name': 1})
                if not result:
                    db.user.insert_one({
                        "email": email,
                        "first_name": first_name,
                        "last_name": last_name,
                        "summary":[],
                        "created_date": datetime.utcnow()
                    })
                    return jsonify({"data" : "Inserted"}),200
                else:
                     return jsonify({"data" : "User Already Exists"})
        except Exception as e:
            print(e)
            return "error"

    def glogin(x):
        try:
            if (x['email'] != ''):
                email = x['email']
                result = db.user.find_one(
                    {"email": email, }, {'_id': 0, 'first_name': 1, 'last_name': 1})
                if (result != None):
                    access_token = create_access_token(identity=email)
                    resp = Response('login successfull', status=200)
                    resp.set_cookie('jwt', access_token,
                                    httponly=True, secure=True,samesite='None')
                    return resp
                else:
                     return jsonify({"data" : "User doesnt exsist"})
            else:
                 return jsonify({"data" : "Sign up first"})
        except Exception as e:
            print(e)
            return "error"
        
    def login(x):
        try:
            if (x['email'] != '' or x['password'] != ''):
                uemail = x['email']
                upassword=x['password']
                result = db.user.find_one(
                    {"email": uemail, }, {'_id': 0, 'first_name': 1, 'last_name': 1,'password': 1})
                if (result != None):
                    if bcrypt.checkpw(upassword.encode('utf-8'), result['password']):
                        access_token = create_access_token(identity=uemail)
                        resp = Response('login successfull', status=200)
                        resp.set_cookie('jwt', access_token,
                                        httponly=True, secure=True,samesite="None")
                        return resp
                    else:
                         return jsonify({"data": "incorrect credentials"})
                else:
                     return jsonify({"data": "User doesnt exsist"})
            else:
                 return jsonify({"data" : "Fill all details"})
        except Exception as e:
            print(e)
            return "error"
        
    def auth():
        try:
            user_id = request.cookies.get('jwt')
            
            if not user_id:
                return jsonify({"error": "Unauthorized"}), 401
            else:
                jwt_payload = jwt.decode(user_id, os.environ.get('JWT_SECRET'), algorithms=['HS256'])
                user_id = jwt_payload['user_id']
                return jsonify({"user_id": user_id}), 200
        except Exception as e:
            print(e)
            return "error"

    def logout():
        try:
            response = jsonify({"msg": "logout successful"})
            unset_jwt_cookies(response)
            return response
        except Exception as e:
            print(e)
            return "error"
        
    def save_summary(u_mail,summ):
        try:
            print(u_mail)
            mail=u_mail
            summary=summ
            result = db.user.find_one(
                    {"email": mail, }, {'_id': 0, 'first_name': 1, 'last_name': 1,'password': 1})
            if (result != None):
                collection = db['mycollection']
                collection.update_one({'_id': 1}, {'$push': {'discussion': summary}})
                return jsonify({"data" : "Inserted"}),200
            else:
                return jsonify({"data": "User doesnt exsist"})
        except Exception as e:
            print(e)
            return "error"
            
