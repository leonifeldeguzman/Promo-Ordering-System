import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("PGHOST"),        
    database=os.getenv("PGDATABASE"),
    user=os.getenv("PGUSER"),         
    password=os.getenv("PGPASSWORD"), 
    port=os.getenv("PGPORT", 5432)    
)