from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from orchestration.task_definition import (task_generate_data, 
                                           task_process_data, 
                                           task_train_model, 
                                           task_scoring_service)

dag = DAG('drone_data_pipeline',
          description='Data pipeline for drone telemetry data',
          schedule_interval='0 12 * * *',
          start_date=datetime(2023, 5, 29),
          catchup=False)

t1 = PythonOperator(
    task_id='generate_data',
    python_callable=task_generate_data,
    dag=dag,
)

t2 = PythonOperator(
    task_id='process_data',
    python_callable=task_process_data,
    dag=dag,
)

t3 = PythonOperator(
    task_id='train_model',
    python_callable=task_train_model,
    dag=dag,
)

t4 = PythonOperator(
    task_id='scoring_service',
    python_callable=task_scoring_service,
    dag=dag,
)

t1 >> t2 >> t3 >> t4  # defines the task dependencies
