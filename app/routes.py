from flask import jsonify, request
from app import app
from app import controllers
@app.route('/convert_text', methods=['GET', 'POST'])
def listen():
    surveyDa = request.get_json()
    return controllers.AudioController.listen(surveyDa)