import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname='Atm_app',
        user='ViraKrajevskiy',
        password='3003',
        host='localhost',
        port='5432'        
    )
