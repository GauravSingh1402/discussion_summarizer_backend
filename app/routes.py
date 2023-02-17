from flask import jsonify, request
from app import app
from app import controllers
from app import services
@app.route('/convert_text', methods=['GET', 'POST'])
def listen():
    surveyDa = request.get_json()
    return controllers.AudioController.listen(surveyDa)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    userData = request.get_json()
    try:
         return controllers.AudioController.signup(userData)
    except:
        print("Error")
        

        
@app.route('/login', methods=['GET', 'POST'])
def login():
    userData = request.get_json()
    try:
         return controllers.AudioController.login(userData)
    except:
        print("Error")
        




@app.route('/summarize', methods=['GET', 'POST'])
def summary():
    text_obj = request.get_json()
    input_text = text_obj['text']
    try:
        return services.Service.listen(input_text)
    except:
        return "Error"