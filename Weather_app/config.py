import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/weather_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
