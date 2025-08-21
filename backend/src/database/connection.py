import psycopg2
from src.config.config import load_config

config = load_config()

conn = psycopg2.connect(
    dbname=config.DB_NAME,
    user=config.DB_USER,
    password=config.DB_PASSWORD,
    host=config.DB_HOST,
    port=config.DB_PORT
)
conn.autocommit = True
cursor = conn.cursor()
