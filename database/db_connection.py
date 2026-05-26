import os
import psycopg2

# Get database URL from Railway (no need for dotenv on Railway)
database_url = os.getenv('DATABASE_URL')

if not database_url:
    raise Exception("DATABASE_URL environment variable not found! Make sure PostgreSQL is linked to this service.")

# Create connection using DATABASE_URL
conn = psycopg2.connect(database_url)