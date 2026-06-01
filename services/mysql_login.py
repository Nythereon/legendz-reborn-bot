import os
import mysql.connector

def login():
    # Connect to MySQL Server
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password=os.getenv('SQL_PASSWORD'),
        database=os.getenv('DATA_BASE')
    )
    return connection