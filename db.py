import sqlite3
from datetime import datetime

DB_NAME = "analytics.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL UNIQUE,
                rating REAL,
                count INTEGER DEFAULT 1,
                total_rating REAL DEFAULT 0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute("UPDATE interactions SET total_rating = rating WHERE total_rating = 0")
        conn.commit()

def log_interaction(topic, rating):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, count, total_rating FROM interactions WHERE topic = ?", (topic,))
        row = cursor.fetchone()
        if row:
            id_, count, total_rating = row
            new_count = count + 1
            new_total_rating = total_rating + rating
            avg_rating = new_total_rating / new_count
            cursor.execute("""
                UPDATE interactions 
                SET count = ?, total_rating = ?, rating = ?, timestamp = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (new_count, new_total_rating, avg_rating, id_))
        else:
            cursor.execute("""
                INSERT INTO interactions (topic, rating, count, total_rating)
                VALUES (?, ?, 1, ?)
            """, (topic, rating, rating))
        conn.commit()

def fetch_metrics():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT SUM(count) FROM interactions")
        total_queries = cursor.fetchone()[0] or 0

        cursor.execute("SELECT topic, count FROM interactions ORDER BY count DESC")
        most_common_topics = cursor.fetchall()

        cursor.execute("SELECT AVG(rating) FROM interactions WHERE rating IS NOT NULL")
        avg_rating = cursor.fetchone()[0] or 0.0

        today = datetime.now().date()
        cursor.execute("SELECT SUM(count) FROM interactions WHERE DATE(timestamp) = ?", (today,))
        today_interactions = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(count) FROM interactions WHERE rating >= 3")
        successful = cursor.fetchone()[0] or 0

        success_rate = round((successful / total_queries) * 100, 2) if total_queries else 0

        cursor.execute("SELECT timestamp, rating FROM interactions WHERE rating IS NOT NULL ORDER BY timestamp DESC LIMIT 100")
        raw_data = cursor.fetchall()

    return {
        "total_queries": total_queries,
        "most_common_topics": most_common_topics,
        "average_rating": avg_rating,
        "today_interactions": today_interactions,
        "success_rate": success_rate,
        "raw_data": raw_data
    }
