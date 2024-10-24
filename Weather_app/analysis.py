from models import db, WeatherData, WeatherStats
from sqlalchemy import func

def calculate_weather_stats():
    results = db.session.query(
        func.extract('year', WeatherData.date).label('year'),
        WeatherData.station_id,
        func.avg(WeatherData.max_temperature).label('avg_max_temp'),
        func.avg(WeatherData.min_temperature).label('avg_min_temp'),
        func.sum(WeatherData.precipitation).label('total_precipitation')
    ).group_by('year', WeatherData.station_id).all()

    for year, station_id, avg_max_temp, avg_min_temp, total_precipitation in results:
        stat = WeatherStats(
            year=int(year),
            station_id=station_id,
            avg_max_temp=avg_max_temp,
            avg_min_temp=avg_min_temp,
            total_precipitation=total_precipitation
        )
        db.session.add(stat)

    db.session.commit()

if __name__ == "__main__":
    from app import app
    with app.app_context():
        calculate_weather_stats()
