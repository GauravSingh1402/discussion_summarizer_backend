from app import app
from app import controllers
@app.route('/convert_text')
def listen():
    return controllers.AudioController.listen('Hey Ohh')