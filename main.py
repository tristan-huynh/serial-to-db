import serial
import sqlite3
import json
import time
import logging
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# add src to python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from connector import DatabaseManager

load_dotenv()

log_level = getattr(logging, os.getenv('LOG_LEVEL', 'INFO').upper())
log_file = os.getenv('LOG_FILE', 'serial_data.log')

logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

def main():
    # env configuration
    SERIAL_PORT = os.getenv('SERIAL_PORT', 'COM3')
    BAUD_RATE = int(os.getenv('BAUD_RATE', '115200'))
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'sensor_data.db')
    # init database
    db_manager = DatabaseManager(DATABASE_PATH)
    db_manager.initialize_database()
    try:
        # open serial
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        logging.info(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud")
        
        while True:
            try:
                # read from serial
                line = ser.readline().decode('utf-8').strip()
                
                if line:
                    logging.info(f"Received: {line}")          
                    try:
                        # parse JSON data
                        data = json.loads(line)
                        
                        # validation
                        if 'timestamp' in data:
                            db_manager.insert_sensor_data(data)
                            logging.info("Data stored successfully")
                        else:
                            logging.warning("Invalid data format - missing timestamp")                            
                    except json.JSONDecodeError as e:
                        logging.error(f"JSON decode error: {e}")
                    except Exception as e:
                        logging.error(f"Database error: {e}")                        
            except Exception as e:
                logging.error(f"Serial read error: {e}")
                time.sleep(1)

    except serial.SerialException as e:
        logging.error(f"Serial connection error: {e}")
    except KeyboardInterrupt:
        logging.info("Stopping data collection...")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            logging.info("Serial connection closed")
        db_manager.close()
        logging.info("Database connection closed")

if __name__ == "__main__":
    main()