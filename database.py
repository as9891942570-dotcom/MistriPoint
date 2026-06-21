import psycopg
from psycopg.rows import dict_row

DATABASE_URL = "postgresql://neondb_owner:YOUR_PASSWORD@ep-summer-brook-atq95usp-pooler.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require"

def get_db_connection():
    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )