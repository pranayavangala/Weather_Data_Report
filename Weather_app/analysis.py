from app import app, db  # Import your Flask app and SQLAlchemy instance
from models import WeatherData  # Ensure your model is correctly imported
from sqlalchemy import extract  # Import the 'extract' function to extract the year from the date

def calculate_weather_stats():
    with app.app_context():  # Use Flask app context
        results = db.session.query(
            extract('year', WeatherData.date).label('year'),  # Extract year from 'date'
            WeatherData.station_id,
            db.func.avg(WeatherData.max_temperature).label('avg_max_temp'),  # Calculate average max temperature
            db.func.avg(WeatherData.min_temperature).label('avg_min_temp'),  # Calculate average min temperature
            db.func.sum(WeatherData.precipitation).label('total_precipitation')  # Sum precipitation
        ).group_by(extract('year', WeatherData.date), WeatherData.station_id).all()

        # Process results as needed
        for result in results:
            print(f"Year: {result.year}, Station ID: {result.station_id}, "
                  f"Avg Max Temp: {result.avg_max_temp}, "
                  f"Avg Min Temp: {result.avg_min_temp}, "
                  f"Total Precipitation: {result.total_precipitation}")

if __name__ == "__main__":
    calculate_weather_stats()  # Call the function to calculate weather stats
