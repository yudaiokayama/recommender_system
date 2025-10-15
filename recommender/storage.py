import redis
import psycopg2
import json
import os
from psycopg2.extras import Json

class RedisStorage:
    """Redis for storing recent events."""
    def __init__(self, redis_url):
        self.client = redis.from_url(redis_url)

    def get_recent_events(self, student_id, num_events=10):
        key = f"events:{student_id}"
        # Get the latest 'num_events' items from the list
        raw_events = self.client.lrange(key, 0, num_events - 1)
        # Decode from bytes and parse from JSON string
        return [json.loads(event.decode('utf-8')) for event in raw_events]

    def push_event(self, event):
        student_id = event.get('student_id')
        if not student_id:
            return
        key = f"events:{student_id}"
        # Push the event to the front of the list
        self.client.lpush(key, json.dumps(event))
        # Keep the list trimmed to a reasonable size (e.g., 100 recent events)
        self.client.ltrim(key, 0, 99)

class PostgresStorage:
    """PostgreSQL for persistent logging of all events."""
    def __init__(self, db_url):
        self.conn = psycopg2.connect(db_url)
        self._create_table_if_not_exists()

    def _create_table_if_not_exists(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS recommendation_logs (
                    id SERIAL PRIMARY KEY,
                    event_data JSONB NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                );
            """)
            self.conn.commit()

    def log_event(self, event):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO recommendation_logs (event_data) VALUES (%s)",
                (Json(event),)
            )
            self.conn.commit()
