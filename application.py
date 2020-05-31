from flask import Flask
from flask import request
from flask import jsonify
app = Flask(__name__)

@app.route("/")
def format_endpoint():
    return jsonify({'generate': 'Use /generate endopoint to generate text that has authors style. You can input a topic for the text',
            'predict': 'Use /predict endpoint to classify a text and predict the author. Use the text key for your input.'})

@app.route("/predict")
def predict_endpoint():
    args = request.args
    text_to_predict = args.get('text')
    prediction = dict(EAP=48, HPL=20, MWS=32, text=text_to_predict)
    return jsonify(prediction)

@app.route("/generate")
def generate_endpoint():
    args = request.args
    topic = args.get('topic')
    
    prediction = dict(EAP="EAP text", HPL="HPL text", MWS="MWS text", topic=topic)
    return jsonify(prediction)