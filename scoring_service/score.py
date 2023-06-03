import pickle
from model_training import MODEL_FILE_PATH

def score_model(data):
    """Score data using the trained model."""
    with open(MODEL_FILE_PATH, 'rb') as file:
        model = pickle.load(file)
    return model.predict(data)
