# Serial to SQLite Database

This project reads JSON sensor data from a serial port and stores it in a SQLite database.

## Data Format

The system expects JSON data in this format:
```json
{"timestamp":2228072,"temperature":,"humidity":,"fan_status":1,"alert_condition":2}
```

Note: Empty temperature and humidity values are handled as NULL in the database.

## Database Schema

The SQLite database contains a `sensor_data` table with the following columns:

- `id`: Auto-incrementing primary key
- `device_timestamp`: Original timestamp from the device
- `received_timestamp`: When the data was received and stored
- `temperature`: Temperature reading (REAL, nullable)
- `humidity`: Humidity reading (REAL, nullable)
- `fan_status`: Fan status (INTEGER)
- `alert_condition`: Alert condition (INTEGER)
- `raw_data`: Original JSON data as text

## Installation

1. Install Python dependencies:
```powershell
pip install -r requirements.txt
```

2. Copy the example environment file and configure it:
```powershell
copy .env.example .env
```

## Configuration

Edit the `.env` file to match your setup:

```env
# Serial Port Configuration
SERIAL_PORT=COM3        # Change to your COM port
BAUD_RATE=115200

# Database Configuration
DATABASE_PATH=sensor_data.db

# Logging Configuration
LOG_LEVEL=INFO          # DEBUG, INFO, WARNING, ERROR
LOG_FILE=serial_data.log
```

### Available Environment Variables:

- `SERIAL_PORT`: COM port to connect to (default: COM3)
- `BAUD_RATE`: Serial communication speed (default: 115200)
- `DATABASE_PATH`: SQLite database file path (default: sensor_data.db)
- `LOG_LEVEL`: Logging verbosity (default: INFO)
- `LOG_FILE`: Log file name (default: serial_data.log)

## Usage

```powershell
python main.py
```

The program will:
- Connect to the specified serial port
- Create the SQLite database if it doesn't exist
- Continuously read and store data
- Log all activities to console and `serial_data.log`

Press Ctrl+C to stop the program.
