# app.py
import os
from decimal import Decimal
from datetime import date, datetime

from flask import Flask, jsonify
import mysql.connector
from mysql.connector import pooling, Error

# ---- Config from env ----
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "mydatabase"),
    "user": os.getenv("DB_USER", "myuser"),
    "password": os.getenv("DB_PASSWORD", "mypassword"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "connection_timeout": 5,
}

# ---- Connection pool ----
pool = pooling.MySQLConnectionPool(pool_name="flaskpool", pool_size=5, **DB_CONFIG)

app = Flask(__name__)

def to_jsonable(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="ignore")
    return value

@app.get("/planets")
def get_planets():
    conn = None
    try:
        conn = pool.get_connection()
        with conn.cursor(dictionary=True) as cur:
            cur.execute("SELECT * FROM planets;")
            rows = cur.fetchall() or []
            result = [{k: to_jsonable(v) for k, v in row.items()} for row in rows]
            return jsonify(result), 200
    except Error as e:
        return jsonify({"error": f"MySQL error: {e}"}), 500
    finally:
        try:
            if conn and conn.is_connected():
                conn.close()
        except Exception:
            pass

@app.get("/healthz")
def healthz():
    conn = None
    try:
        conn = pool.get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
        return jsonify({"status": "ok"}), 200
    except Error as e:
        return jsonify({"status": "down", "error": str(e)}), 500
    finally:
        try:
            if conn and conn.is_connected():
                conn.close()
        except Exception:
            pass

if __name__ == "__main__":
    # For local testing only — on OpenShift use gunicorn in the container CMD
    app.run(host="0.0.0.0", port=8080)
