from fastapi import FastAPI, HTTPException
import redis
import psycopg2

app = FastAPI()

# Redis initialization with error handling
try:
    r = redis.Redis(host="redis", port=6379, decode_responses=True)
    r.ping()
except Exception as e:
    raise RuntimeError(f"Could not connect to Redis: {e}")

# Postgres initialization
try:
    conn = psycopg2-binary.connect(
        host="db",
        database="demo",
        user="demo",
        password="password"
    )
    cur = conn.cursor()
except Exception as e:
    raise RuntimeError(f"Could not connect to Postgres: {e}")


@app.get("/cache/{key}")
def cache_get(key: str):
    try:
        val = r.get(key)
        return {"key": key, "value": val}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis GET error: {e}")


@app.post("/cache/{key}/{value}")
def cache_set(key: str, value: str):
    try:
        r.set(key, value)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis SET error: {e}")


@app.get("/db/{table}")
def db_get(table: str):
    try:
        cur.execute(f"SELECT * FROM {table} LIMIT 5;")
        rows = cur.fetchall()
        return {"rows": rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Postgres error: {e}")


@app.get("/")
def root():
    return {"message": "Hello from Bootcamp Day 3"}
