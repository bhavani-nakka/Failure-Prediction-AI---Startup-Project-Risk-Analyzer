import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="ml_project",
        user="postgres",
        password="bhavani",
        port="5432"
    )