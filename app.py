from flask import Flask
from flask_restful import Resource, Api
from flask import request

app = Flask(__name__)
api = Api(app)

class Format(Resource):
    def get(self):
        return {'generate': 'Use /generate endopoint to generate text that has authors style. You can input a topic for the text',
                'predict': 'Use /predict endpoint to classify a text and predict the author. Use the text key for your input.'}

class Predict(Resource):
    def get(self):
        args = request.args
        print (args) # For debugging
        text_to_predict = args.get('text')
        prediction = dict(EAP=48, HPL=20, MWS=32, text=text_to_predict)
        return prediction

class Generate(Resource):
    def get(self):
        args = request.args
        print (args) # For debugging
        
        topic = args.get('topic')
        
        prediction = dict(EAP="EAP text", HPL="HPL text", MWS="MWS text", topic=topic)
        return prediction

api.add_resource(Format, '/')
api.add_resource(Predict, '/predict')
api.add_resource(Generate, '/generate')

if __name__ == '__main__':
    app.run(debug=True)