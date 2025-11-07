
from fastapi import FastAPI
import redis
import psycopg2
from psycopg2 import OperationalError

app = FastAPI()


try:
    r = redis.Redis(host="redis", port=6379, decode_responses=True)
    r.ping()
except Exception as e:
    r = None
    print(f"Redis connection error: {e}")


def get_pg_conn():
    try:
        conn = psycopg2.connect(
            host="db",
            database="demo",
            user="demo",
            password="password"
        )
        return conn
    except OperationalError as e:
        print(f"Postgres connection error: {e}")
        return None



@app.get("/cache/{key}")
def cache_get(key: str):
    if not r:
        return {"error": "Redis not available"}
    try:
        val = r.get(key)
        if val is None:
            return {"error": "Key not found"}
        return {"key": key, "value": val}
    except Exception as e:
        return {"error": str(e)}



@app.post("/cache/{key}/{value}")
def cache_set(key: str, value: str):
    if not r:
        return {"error": "Redis not available"}
    try:
        r.set(key, value)
        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}



@app.get("/")
def root():
    return {"message": "Hello from Bootcamp Day 3"}
