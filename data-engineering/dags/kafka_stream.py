from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2024, 7, 7, 10, 00)
}

def get_data():
    import requests

    res = requests.get('https://randomuser.me/api/')
    res = res.json()
    res = res['results'][0]

def format_data(res):
    data = {}
    location = res['location']
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']} 
                      f" {location['city']} {location['state']} {location['country']}

def stream_data():
    import json
    
    print(json.dumps(res, indent=3))

with DAG('user_automation',
         default_args=default_args,
         schedule='@daily',
         catchup=False) as dag:
    
    streaming_task = PythonOperator(
        task_id='stream_data_from_api',
        python_callable=stream_data
    )

stream_data()