from fastapi import FastAPI, HTTPException
import redis
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI()

# Redis initialization with error handling
try:
    r = redis.Redis(host="redis", port=6379, decode_responses=True)
    r.ping()  # Test connection
except redis.ConnectionError:
    r = None

# PostgreSQL connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="db",
            database="demo",
            user="demo",
            password="password",
            cursor_factory=RealDictCursor
        )
        return conn
    except psycopg2.Error:
        return None

@app.get("/cache/{key}")
def cache_get(key: str):
    if not r:
        raise HTTPException(status_code=503, detail="Redis not available")
    try:
        val = r.get(key)
        return {"key": key, "value": val}
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")

@app.post("/cache/{key}/{value}")
def cache_set(key: str, value: str):
    if not r:
        raise HTTPException(status_code=503, detail="Redis not available")
    try:
        r.set(key, value)
        return {"status": "ok"}
    except redis.RedisError as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")

@app.get("/db/test")
def db_test():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=503, detail="Database not available")
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            result = cur.fetchone()
        conn.close()
        return {"database": "connected", "version": result["version"]}
    except psycopg2.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/")
def root():
    return {"message": "Hello from Bootcamp Day 3"}
