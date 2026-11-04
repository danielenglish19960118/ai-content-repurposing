"""
SQLite Storage for Telemetry & Audit Logging
"""
import sqlite3
import time

DB_PATH = "telemetry.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id TEXT,
            timestamp REAL,
            char_count INTEGER,
            est_tokens INTEGER,
            est_cost_usd REAL,
            latency_sec REAL
        )
    """)
    conn.commit()
    conn.close()

def log_usage(tenant_id: str, char_count: int, tokens: int, cost: float, latency: float):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usage_logs (tenant_id, timestamp, char_count, est_tokens, est_cost_usd, latency_sec)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (tenant_id, time.time(), char_count, tokens, cost, latency))
    conn.commit()
    conn.close()
