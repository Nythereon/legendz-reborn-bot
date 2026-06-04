import os
from datetime import datetime


def logger(error_location: str, error_message: str):
    os.makedirs('logs', exist_ok=True)

    dt_obj = datetime.now()
    date = dt_obj.date()
    date_time = dt_obj.strftime('%Y-%m-%d %H:%M:%S')

    with open(f'logs/{date}.log', 'a') as file:
        file.write(f'{date_time} | {error_location} | {error_message}\n')
