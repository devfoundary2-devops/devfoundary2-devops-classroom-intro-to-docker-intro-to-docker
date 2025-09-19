
from fastapi import FastAPI, HTTPException
import redis
import psycopg2

app = FastAPI()
r = redis.Redis(host="redis", port=6379)

conn = psycopg2.connect(
        host="pg",
        database="demo",
        user="demo",
        password="password"
)
cur = conn.cursor()

@app.get("/cache/{key}")
def read_cache(key: str):
    try:
        value = r.get(key)
        if value is None:
            return {"error": f"No cache found for key '{key}'"}
        return {"message": value.decode("utf-8")}
    except redis.RedisError as e:
        return {"message": str(e)}

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


@app.post("/users/{name}")
def create_user(name: str):
    try:
        cur.execute("INSERT INTO users (name) VALUES (%s) RETURNING id;", (name,))
        conn.commit()
        user_id = cur.fetchone()[0]
        return {"id": user_id, "name": name}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users")
def list_users():
    cur.execute("SELECT id, name FROM users;")
    rows = cur.fetchall()
    return {"users": [{"id": r[0], "name": r[1]} for r in rows]}

