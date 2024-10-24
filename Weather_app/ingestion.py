import os
import logging
from datetime import datetime
import psycopg2

# Configure logging
logging.basicConfig(level=logging.INFO)

def connect_db():
    """Connect to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="weather_db",
            user="postgres",
            password="postgres"
        )
        return conn
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        raise

def ingest_weather_data():
    conn = connect_db()
    cursor = conn.cursor()
    start_time = datetime.now()
    records_ingested = 0

    for filename in os.listdir('wx_data'):
        if filename.endswith('.txt'):
            with open(os.path.join('wx_data', filename), 'r') as file:
                for line in file:
                    parts = line.strip().split('\t')
                    if len(parts) != 4:  # Ensure there are exactly 4 parts
                        logging.warning(f"Skipping malformed line: {line.strip()}")
                        continue  # Skip this line and move to the next

                    date_str, max_temp_str, min_temp_str, precip_str = parts
                    date = datetime.strptime(date_str, '%Y%m%d').date()
                    max_temp = float(max_temp_str) if max_temp_str != '-9999' else None
                    min_temp = float(min_temp_str) if min_temp_str != '-9999' else None
                    precip = float(precip_str) / 10.0 if precip_str != '-9999' else None  # Convert to mm

                    try:
                        cursor.execute(
                            """INSERT INTO weather_data (date, station_id, max_temperature, min_temperature, precipitation)
                               VALUES (%s, %s, %s, %s, %s)
                               ON CONFLICT (date, station_id) DO NOTHING""",
                            (date, filename[:-4], max_temp, min_temp, precip)
                        )
                        records_ingested += cursor.rowcount
                    except Exception as e:
                        logging.error(f"Error inserting record {line.strip()}: {e}")
                        conn.rollback()  # Roll back the transaction on error
                        continue  # Skip to the next record

            conn.commit()  # Commit after processing the entire file

    cursor.close()
    conn.close()
    end_time = datetime.now()
    logging.info(f"Ingestion completed in {end_time - start_time}. Records ingested: {records_ingested}")

if __name__ == "__main__":
    ingest_weather_data()
