from flask import jsonify, request
from app import app
from app import controllers
from app import services
from app import models

@app.route('/', methods=['GET', 'POST'])
def listen():
    return jsonify({"message":'Successfully running'})

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
        
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    try:
         return controllers.AudioController.logout()
    except:
        print("Error")
        
        
@app.route('/auth', methods=['GET', 'POST'])
def auth():
    try:
         return controllers.AudioController.auth()
    except:
        print("Error")
        




@app.route('/summarize', methods=['GET', 'POST'])
def summary():
    text_obj = request.get_json()
    input_text = text_obj['text']
    stop_words = text_obj['limit']
    top = text_obj['top']
    num_sent = text_obj['num_sent']
    print(top)
    try:
        processed_text = services.Service.listen(input_text)
        # gpt = models.SummarizerModel.gpt(input_text)
        lsa = models.SummarizerModel.lsa(input_text,num_sent)
        kl = models.SummarizerModel.kl(input_text,num_sent)
        
        summary = {
            'lsa': lsa,
            'kl':kl
        }
        return jsonify({"summary": summary}),200
    except Exception as e:
        print("Error: ", e)
        return "Error occurred while summarizing the text."