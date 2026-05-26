import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Get database URL from Railway
database_url = os.getenv('DATABASE_URL')

if not database_url:
    raise Exception("DATABASE_URL environment variable not found!")

def get_db_connection():
    """Create and return a new database connection"""
    conn = psycopg2.connect(database_url)
    return conn

def get_db_cursor():
    """Get a cursor with RealDictCursor for named columns"""
    conn = get_db_connection()
    return conn, conn.cursor(cursor_factory=RealDictCursor)