from flask import Flask, request
from score import score_model

app = Flask(__name__)
SCORING_SERVICE_URL = 'http://localhost:5000'
@app.route('/score', methods=['POST'])
def score():
    """Score the input data and return the prediction."""
    data = request.json['data']
    prediction = score_model(data)
    return {'prediction': prediction}
