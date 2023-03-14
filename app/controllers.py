from flask import jsonify, request, session, Response,url_for,redirect,send_file
# from app import app
from app import db
from app import mail
from datetime import datetime
from flask_session import Session
import bcrypt
import base64
import os
from flask_bcrypt import check_password_hash
from flask_jwt_extended import decode_token,create_access_token, get_jwt, get_jwt_identity,unset_jwt_cookies, jwt_required, JWTManager,unset_access_cookies, unset_refresh_cookies
from flask_mail import Mail, Message
import hashlib
import io
from datetime import datetime, timedelta


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
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
                hashed_password_str = base64.b64encode(hashed_password).decode('utf-8')
                result = db.user.find_one(
                    {"email": email, }, {'_id': 0, 'first_name': 1, 'last_name': 1})
                if not result:
                    db.user.insert_one({
                        "email": email,
                        "first_name": first_name,
                        "last_name": last_name,
                        "password": hashed_password_str,
                        "summary":[],
                        "photo":" ",
                        "isGoogle": False,
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
                photo=x['photo']
                result = db.user.find_one(
                    {"email": email, }, {'_id': 0, 'first_name': 1, 'last_name': 1})
                if not result:
                    db.user.insert_one({
                        "email": email,
                        "first_name": first_name,
                        "last_name": last_name,
                        "summary":[],
                        "isGoogle": True,
                        "photo":photo,
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
                    {"email": email, }, {'_id': 0, 'first_name': 1, 'last_name': 1,'isGoogle':1})
                if (result != None and result['isGoogle']==True):
                    access_token = create_access_token(identity=email)
                    resp = Response('login successfull', status=200)
                    resp.set_cookie('jwt', access_token,
                                    httponly=True, path='/',secure=True,samesite='None')
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
                    {"email": uemail, }, {'_id': 0, 'first_name': 1, 'last_name': 1,'password': 1,'isGoogle':1})
                if (result != None and result['isGoogle']==False):
                    hashed_password = base64.b64decode(result['password'])
                    if bcrypt.checkpw(upassword.encode('utf-8'), hashed_password):
                        access_token = create_access_token(identity=uemail)
                        resp = Response('login successfull', status=200)
                        resp.set_cookie('jwt', access_token,
                                        httponly=True, path='/',secure=True,samesite="None")
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
                return jsonify({"data": "Unauthorized"})
            else:
                jwt_payload = decode_token(user_id)
                user_id = jwt_payload['sub']
                result = db.user.find_one(
                    {"email": user_id}, {'_id': 0, 'first_name': 1, 'last_name': 1,'summary':1,'isGoogle':1,'photo':1})

                return jsonify({"user_id": user_id,"other_info":result}), 200
        except Exception as e:
            print(e)
            return "error"

    def logout():
        try:
            resp = Response('logout successfull', status=200)
            try:
                resp.set_cookie('jwt', '', max_age=0, path='/',httponly=True,secure=True,samesite="None")
                return resp
            except Exception as e:
                print(e)
                print("cant delete cookie")
                return "error occured"
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
        
    def download_summary(text):
        print(text)
        try:
            with io.StringIO(text) as f:
                # Create an in-memory file object and write the summary text to it
                # We use StringIO instead of a regular file object since we don't need to save the file to disk
                file_content = f.read()
                file_content_base64 = base64.b64encode(file_content.encode('utf-8'))
                return file_content_base64.decode('utf-8')
        except Exception as e:
            print(e)
            return "error"
            
        
        
        
    def eprofile(udata):
        user_data=udata
        print(user_data)
        email=user_data["email"]
        umail=user_data["umail"]
        name=user_data["name"]
        password=user_data["password"]
        npassword=user_data["npassword"]
        cpassword=user_data["cpassword"]
        photo=user_data["image"]
        print(cpassword,email,name,password,npassword)
        try:
            if email!=None and email!=" ":
                if umail!=" ":
                    print('Mail',umail)
                    try:
                        if umail != " ":
                            result = db.user.find_one({"email": email}, {'_id': 0, 'first_name': 1, 'last_name': 1,'password': 1})
                            if result is not None:
                                try:
                                    db.user.update_one({'email': email}, {'$set': {'email': umail}})
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
                elif photo!=" ":
                    try:
                        if email!=" ":
                            result = db.user.find_one({"email": email}, {'_id': 0, 'first_name': 1, 'last_name': 1,'password': 1})
                            if result is not None:
                                try:
                                    db.user.update_one({'email': email}, {'$set': {'photo': photo}})
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
                elif name!=" ":
                    print('NAME',name)
                    first_name=name[:name.index(" ")]
                    last_name=name[name.index(" ")+1:]
                    print(first_name, last_name)
                    try:
                        if email!=" ":
                            result = db.user.find_one({"email": email}, {'_id': 0, 'first_name': 1, 'last_name': 1,'password': 1})
                            if result is not None:
                                try:
                                    db.user.update_one({'email': email}, {'$set': {'first_name': first_name, 'last_name': last_name}})
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
                elif password!=" " and len(cpassword)>0 and len(npassword)>0 :
                    print('entered password')
                    try:
                        if (cpassword==npassword and email!=" " and email!=None):
                            result = db.user.find_one(
                                {"email": email, }, {'_id': 0, 'first_name': 1, 'last_name': 1,'password': 1})
                            if (result != None):
                                if result['password']!=None and result['password']!=" ":
                                    salt = bcrypt.gensalt()
                                    hashed_password = base64.b64decode(result['password'])
                                    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                                        uhashed_password = bcrypt.hashpw(npassword.encode('utf-8'), salt)
                                        hashed_password_str = base64.b64encode(uhashed_password).decode('utf-8')
                                        db.user.update_one({'email': email}, {'$set': {'password': hashed_password_str}})
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
                else:
                    print("Unauthorized")
                    return jsonify({"data": "Unauthorized"})
        except Exception as e:
            print(e)
            return "error"
        
     
    
    
    def forgot_password(email):
        e_mail=email
        try:
            token = create_access_token(identity=email)
            msg = Message('Reset Your Password', sender=os.environ.get('MAIL_USERNAME'), recipients=[e_mail])
            msg.body = f"Click the link to reset your password: https://summa-sense.vercel.app/reset_password/{token}"
            mail.send(msg)
            return jsonify({"data": "success"})
        except Exception as e:
            print(e)
            return "error"
        
    def reset_password(password,cpassword,token):
        tok=token
        passw=password
        try:
            uemail = get_jwt_identity()
        except Exception as e:
            print('error',e)
            return "error"
        try:
            result = db.user.find_one(
                    {"email": uemail, }, {'_id': 0, 'first_name': 1, 'last_name': 1,'password': 1})
            if (result != None):
                if result['password']!=None and result['password']!=" ":
                    if(passw==cpassword):
                        salt = bcrypt.gensalt()
                        uhashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
                        hashed_password_str = base64.b64encode(uhashed_password).decode('utf-8')
                        db.user.update_one({'email': uemail}, {'$set': {'password': hashed_password_str}})
                    else:
                        return jsonify({'data': 'Passwords do not match'})
                    return jsonify({"data": "Updated"})
                else:
                    return jsonify({"data": "Google"})
            else:
                return jsonify({"data": "User doesnt exsist"})
        except Exception as e:
            print(e)
            return "error"

  
