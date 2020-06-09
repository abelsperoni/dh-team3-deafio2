from flask import Flask
from flask import request
from flask import jsonify
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
import pickle
app = Flask(__name__)

with open("embedding_model_json.json") as embedding_json:
    embedding_model_json = embedding_json.read()

embedding_model = model_from_json(embedding_model_json)
embedding_model.load_weights('embedding_model_weights.h5') 

with open("generator_json.json") as generator_json:
    generator_model_json = generator_json.read()

generator_model = model_from_json(generator_model_json)
generator_model.load_weights('generator_weights.h5') 

with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

phrases_len = 30

def generate_text(text):
    sequence = tokenizer.texts_to_sequences([text,])
    sequence_padded = pad_sequences(sequence, maxlen=phrases_len)
    generated_text = ''
    for _ in range(30):
        generated_embedded = embedding_model.predict(sequence_padded.reshape(1,30))
        predicted_word_sequence = generator_model.predict(generated_embedded[:,:-1,:])
        #next_index = sample(predicted_word_sequence, 1)
        next_index = predicted_word_sequence.argmax()
        sequence_padded = np.append(sequence_padded,next_index)[1:]

        next_word = tokenizer.sequences_to_texts([[next_index,],])[0]
        generated_text = str(generated_text) + ' ' + next_word
    return generated_text

@app.route("/")
def format_endpoint():
    return jsonify({'generate': 'Use /generate endopoint to generate text that has authors style. You have to input a random text as a seed (text_seed)',
            'predict': 'Use /predict endpoint to classify a text and predict the author. Use the text key for your input.'})

@app.route("/predict")
def predict_endpoint():
    args = request.args
    text_to_predict = args.get('text',)
    prediction = dict(EAP=48, HPL=20, MWS=32, text=text_to_predict)
    return jsonify(prediction)

@app.route("/generate")
def generate_endpoint():
    args = request.args
    text_seed = args.get('text_seed','your acting is very natural as i live')
    generated_text = generate_text(text_seed)
    prediction = dict(generated_text=generated_text, text_seed=text_seed)
    return jsonify(prediction)