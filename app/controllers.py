from flask import jsonify, request
from app import app
from app import db
from datetime import datetime
class AudioController:
    def listen(x):
        return x
    def signup(x):
        try:
            if(x['email']!='' or x['first_name']!='' or x['last_name']!=''):
                email = x['email']
                first_name = x['first_name']
                last_name = x['last_name']
                print(email,first_name,last_name)
                result =  db.user.find_one({"email":email,},{'_id': 0, 'first_name': 1, 'last_name': 1})
                if not result:
                    db.user.insert_one({
                    "email":email,
                    "first_name":first_name,
                    "last_name":last_name,
                    "created_date": datetime.utcnow()
                    })
                    return "Inserted"
                else:
                    return "User Already Exists"
            else:
                return "Fill All The Details"
        except Exception as e:
            print(e)
            return "error"
    def login(x):
        try:
            if(x['email']!=''):
                email = x['email']
                result =  db.user.find_one({"email":email,},{'_id': 0, 'first_name': 1, 'last_name': 1})
            return result
        except Exception as e:
            print(e)
            return "error"