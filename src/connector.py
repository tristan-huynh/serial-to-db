import sqlite3
import logging
from datetime import datetime
from typing import Dict, Any, Optional

class DatabaseManager:
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
        
    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            return True
        except sqlite3.Error as e:
            logging.error(f"Database connection error: {e}")
            return False
    
    def initialize_database(self):
        if not self.connect():
            raise Exception("Failed to connect to database")
            
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    device_timestamp INTEGER NOT NULL,
                    received_timestamp TEXT NOT NULL,
                    temperature REAL,
                    humidity REAL,
                    fan_status INTEGER,
                    alert_condition INTEGER,
                    raw_data TEXT NOT NULL
                )
            ''')
            
            # create index for faster queries
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_device_timestamp 
                ON sensor_data(device_timestamp)
            ''')
            
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_received_timestamp 
                ON sensor_data(received_timestamp)
            ''')
            self.connection.commit()
            logging.info("Database initialized successfully")
        except sqlite3.Error as e:
            logging.error(f"Database initialization error: {e}")
            raise
    
    def insert_sensor_data(self, data: Dict[str, Any]) -> Optional[int]:
        if not self.connection:
            if not self.connect():
                return None
        try:
            cursor = self.connection.cursor()
            # Extract values with defaults
            device_timestamp = data.get('timestamp')
            temperature = data.get('temperature') if data.get('temperature') != '' else None
            humidity = data.get('humidity') if data.get('humidity') != '' else None
            fan_status = data.get('fan_status')
            alert_condition = data.get('alert_condition')
            received_timestamp = datetime.now().isoformat()
            raw_data = str(data)
            
            cursor.execute('''
                INSERT INTO sensor_data 
                (device_timestamp, received_timestamp, temperature, humidity, 
                 fan_status, alert_condition, raw_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (device_timestamp, received_timestamp, temperature, humidity,
                  fan_status, alert_condition, raw_data))
            
            self.connection.commit()
            row_id = cursor.lastrowid
            logging.info(f"Data inserted with ID: {row_id}")
            return row_id
        except sqlite3.Error as e:
            logging.error(f"Database insert error: {e}")
            return None
    
    def get_recent_data(self, limit: int = 100) -> list:
        if not self.connection:
            if not self.connect():
                return []
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT * FROM sensor_data 
                ORDER BY received_timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logging.error(f"Database query error: {e}")
            return []
    def get_data_by_timerange(self, start_time: str, end_time: str) -> list:
        if not self.connection:
            if not self.connect():
                return []
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT * FROM sensor_data 
                WHERE received_timestamp BETWEEN ? AND ?
                ORDER BY received_timestamp ASC
            ''', (start_time, end_time))
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            logging.error(f"Database query error: {e}")
            return []
    def get_statistics(self) -> Dict[str, Any]:
        if not self.connection:
            if not self.connect():
                return {}
        try:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_records,
                    MIN(received_timestamp) as first_record,
                    MAX(received_timestamp) as last_record,
                    AVG(temperature) as avg_temperature,
                    AVG(humidity) as avg_humidity
                FROM sensor_data
            ''')
            result = cursor.fetchone()
            return dict(result) if result else {}
            
        except sqlite3.Error as e:
            logging.error(f"Database query error: {e}")
            return {}
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            logging.info("Database connection closed")