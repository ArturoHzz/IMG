import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # Cambia esto
        password="dex234feR", # Cambia esto
        database="img",
        port=3306
    )
