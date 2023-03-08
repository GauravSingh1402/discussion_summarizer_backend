from flask import jsonify, request, session, Response
# from app import app
from app import db
from datetime import datetime
from flask_session import Session
import bcrypt
import os
from flask_bcrypt import check_password_hash
from flask_jwt_extended import decode_token,create_access_token, get_jwt, get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager
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
            print(user_id)
            if not user_id:
                return jsonify({"data": "Unauthorized"})
            else:
                jwt_payload = decode_token(user_id)
                user_id = jwt_payload['sub']
                result = db.user.find_one(
                    {"email": user_id}, {'_id': 0, 'first_name': 1, 'last_name': 1,'summary':1})
                print(result)
                return jsonify({"user_id": user_id,"other_info":result}), 200
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
        
    def save_summary(u_mail, summ):
        mail=u_mail
        summary=summ
        try:
            if mail != '' and mail is not None:
                result = db.user.find_one({"email": mail}, {'_id': 0, 'first_name': 1, 'last_name': 1,'password': 1})
                if result is not None:
                    try:
                        db.user.update_one({'email': mail}, {'$push': {'summary': summary}})
                        return jsonify({"data":"Updated"}), 200
                    except Exception as e:
                        print(e)
                        return "error"
                else:
                    return jsonify({"data": "User doesn't exist"})
            else:
                return jsonify({"data": "Fill all details"})
        except Exception as e:
            print(e)
            return "error"
        
        
        
    def eprofile(udata):
        print(udata)
        email=udata["email"]
        umail=udata['umail']
        name=udata['name']
        password=udata['password']
        npassword=udata['npassword']
        cpassword=udata['cpassword']
        try:
            if umail!=" " and email!=" " and email!= None:
                try:
                    if umail != '' and umail is not None:
                        result = db.user.find_one({"email": email}, {'_id': 0, 'first_name': 1, 'last_name': 1,'password': 1})
                        if result is not None:
                            try:
                                db.user.update_one({'email': email}, {'$push': {'email': umail}})
                                return jsonify({"data":"Updated"}), 200
                            except Exception as e:
                                print(e)
                                return "error"
                        else:
                            return jsonify({"data": "User doesn't exist"})
                    else:
                        return jsonify({"data": "Fill all details"})
                except Exception as e:
                    print(e)
                    return "error"
            if name!=" " and email!=" " and email!= None:
                first_name=name[:name.index("")]
                last_name=name[name.index(" ")+1:]
                try:
                    if email!='' and email is not None:
                        result = db.user.find_one({"email": email}, {'_id': 0, 'first_name': 1, 'last_name': 1,'password': 1})
                        if result is not None:
                            try:
                                db.user.update_one({'email': email}, {'$push': {'first_name': first_name}})
                                db.user.update_one({'email': email}, {'$push': {'last_name': last_name}})
                                return jsonify({"data":"Updated"}), 200
                            except Exception as e:
                                print(e)
                                return "error"
                        else:
                            return jsonify({"data": "User doesn't exist"})
                    else:
                        return jsonify({"data": "Fill all details"})
                except Exception as e:
                    print(e)
                    return "error"
            if password!=" " and cpassword.length>0 and npassword.length>0 :
                try:
                    if (cpassword==npassword and email!=" " and email!=None):
                        result = db.user.find_one(
                            {"email": email, }, {'_id': 0, 'first_name': 1, 'last_name': 1,'password': 1})
                        if (result != None):
                            if result['password']!=None and result['password']!=" ":
                                if bcrypt.checkpw(password.encode('utf-8'), result['password']):
                                    hashed_password=bcrypt.hashpw(npassword.encode('utf-8'), bcrypt.gensalt())
                                    print(hashed_password)
                                    db.user.update_one({'email': email}, {'$push': {'password': hashed_password}})
                                    return jsonify({"data": "Updated"})
                                else:
                                    return jsonify({"data": "incorrect credentials"})
                            else:
                                return jsonify({"data": "Google"})
                        else:
                            return jsonify({"data": "User doesnt exsist"})
                    else:
                        return jsonify({"data" : "Fill all details"})
                except Exception as e:
                    print(e)
                    return "error"
        except Exception as e:
            print(e)
            return "error"

            
