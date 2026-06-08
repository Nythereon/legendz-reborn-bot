import mysql.connector
import os
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()

def login():
    # Connect to MySQL Server
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user=os.getenv('SQL_USERNAME'),
            password=os.getenv('SQL_PASSWORD'),
            database=os.getenv('DATA_BASE')
        )
    except Exception as error:
        logger('sql_login', str(error))
        return None

    return connection