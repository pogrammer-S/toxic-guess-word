import psycopg2

conn = psycopg2.connect(
    dbname="your_db",
    user="your_user",
    password="your_password",
    host="localhost"
)
conn.autocommit = True
cursor = conn.cursor()
