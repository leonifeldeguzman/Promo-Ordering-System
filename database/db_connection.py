import os
import psycopg2

def db_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise Exception("DATABASE_URL not found")

    return psycopg2.connect(database_url)