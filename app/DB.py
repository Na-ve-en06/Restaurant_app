import psycopg2
import psycopg2.extras
from fastapi import HTTPException
from app.config import settings  # ✅ import settings from config

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=settings.database_hostname,
            database=settings.database_name,
            user=settings.database_username,
            password=settings.database_password,
            port=settings.database_port,
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        return conn
    except Exception as e:
        print("❌ Database connection failed:", str(e))
        raise HTTPException(status_code=500, detail="Could not connect to the database")

