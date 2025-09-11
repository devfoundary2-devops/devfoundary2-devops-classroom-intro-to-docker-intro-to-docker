from fastapi import FastAPI, HTTPException
import redis
import psycopg2
import os

app = FastAPI()

# Redis initialization with error handling
try:
    r = redis.Redis(
        host=os.getenv("REDIS_HOST", "redis"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        decode_responses=True  # auto-decode to str
    )
    r.ping()  # check connection
except redis.exceptions.ConnectionError:
    r = None

# Postgres initialization
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB", "appdb"),
            user=os.getenv("POSTGRES_USER", "appuser"),
            password=os.getenv("POSTGRES_PASSWORD", "apppass"),
            host=os.getenv("POSTGRES_HOST", "db"),
            port=int(os.getenv("POSTGRES_PORT", 5432)),
        )
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Postgres connection error: {e}")


@app.get("/cache/{key}")
def cache_get(key: str):
    if not r:
        raise HTTPException(status_code=500, detail="Redis not available")
    try:
        val = r.get(key)
        if val is None:
            raise HTTPException(status_code=404, detail="Key not found")
        return {"key": key, "value": val}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {e}")


@app.post("/cache/{key}/{value}")
def cache_set(key: str, value: str):
    if not r:
        raise HTTPException(status_code=500, detail="Redis not available")
    try:
        r.set(key, value)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {e}")


@app.get("/db")
def db_test():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT NOW();")
    result = cur.fetchone()
    cur.close()
    conn.close()
    return {"postgres_time": result[0]}


@app.get("/")
def root():
    return {"message": "Hello from Bootcamp Day 3"}
