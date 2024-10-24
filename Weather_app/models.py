from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WeatherData(db.Model):
    __tablename__ = 'weather_data'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    station_id = db.Column(db.String)
    max_temperature = db.Column(db.Float)  # Make sure this matches
    min_temperature = db.Column(db.Float)  # Make sure this matches
    precipitation = db.Column(db.Float)  # Make sure this matches

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class WeatherStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    station_id = db.Column(db.String(50), nullable=False)
    avg_max_temp = db.Column(db.Float)
    avg_min_temp = db.Column(db.Float)
    total_precipitation = db.Column(db.Float)
