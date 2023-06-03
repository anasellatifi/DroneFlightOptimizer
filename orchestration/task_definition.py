from data_generator import generate_data
from data_processor import process_data
from model_training import train_model
from data_transformation import get_processed_data
import requests
from scoring_service import SCORING_SERVICE_URL

def task_generate_data(ti):
    """Apache Airflow task for drone data generation"""
    generate_data()

def task_process_data(ti):
    """Apache Airflow task for data processing"""
    process_data()

def task_train_model(ti):
    """Apache Airflow task for model training"""
    train_model()

def task_scoring_service(ti):
    """Apache Airflow task to ensure the scoring service is running"""
    response = requests.get(SCORING_SERVICE_URL)
    if response.status_code != 200:
        raise Exception('Scoring service is not running')
    
def task_score_data(ti):
    """Apache Airflow task for scoring data"""
    data = get_processed_data() 
    response = requests.post(SCORING_SERVICE_URL + '/score', json={'data': data})
    score = response.json()['prediction']
    return score


