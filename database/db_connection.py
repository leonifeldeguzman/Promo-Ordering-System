import os
import psycopg2

# Get database URL from Railway
database_url = os.getenv('DATABASE_URL')

if not database_url:
    raise Exception("DATABASE_URL environment variable not found! Make sure PostgreSQL is linked.")

# Create the connection
conn = psycopg2.connect(database_url)