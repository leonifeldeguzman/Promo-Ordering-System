import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def db_connection():

    database_url = os.getenv("DATABASE_URL")

    print("DATABASE_URL =", database_url)

    if database_url:
        print("Using Railway DB")
        return psycopg2.connect(database_url)

    print("Using Local DB")

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )