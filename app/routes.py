from flask import jsonify, request
from app import app
from app import controllers
@app.route('/convert_text', methods=['GET', 'POST'])
def listen():
    surveyDa = request.get_json()
    return controllers.AudioController.listen(surveyDa)

@app.route('/signup', methods=['POST'])
def signup():
    userData = request.get_json()
    try:
         return controllers.AudioController.signup(userData)
    except:
        print("Error")

@app.route('/login', methods=['POST'])
def login():
    userData = request.get_json()
    try:
         return controllers.AudioController.login(userData)
    except:
        print("Error")