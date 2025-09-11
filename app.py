from fastapi import FastAPI
import redis
import psycopg2
import os

app = FastAPI()
r = redis.Redis(host="redis", port=6379, decode_responses=True)
# Database connection settings

DB_HOST = os.getenv("DB_HOST", "db")   # "db" is the service name from docker-compose
DB_NAME = os.getenv("POSTGRES_DB", "demo")
DB_USER = os.getenv("POSTGRES_USER", "demo")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")
DB_PORT = os.getenv("DB_PORT", "5432")

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
@app.post('/users')
def create_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, name TEXT);")
    cur.execute("INSERT INTO users (name) VALUES ('Alice'), ('Bob') ON CONFLICT DO NOTHING;")
    conn.commit()
    return {"sucess": "ok"}

@app.get("/users")
def get_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return {"users": rows}



@app.get("/cache/{key}")
def cache_get(key: str):
    val = r.get(key)
    return {"key": key, "value": val}


@app.post("/cache/{key}/{value}")
def cache_set(key: str, value: str):
    r.set(key, value)
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Hello from Bootcamp Day 3"}
