from flask import Blueprint, jsonify, request
from models import WeatherData, WeatherStats

main = Blueprint('main', __name__)

@main.route('/api/weather', methods=['GET'])
def get_weather_data():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    station_id = request.args.get('station_id', None)

    query = WeatherData.query
    if station_id:
        query = query.filter_by(station_id=station_id)

    results = query.paginate(page, per_page, error_out=False)
    return jsonify({'data': [record.as_dict() for record in results.items], 'total': results.total})

@main.route('/api/weather/stats', methods=['GET'])
def get_weather_stats():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    results = WeatherStats.query.paginate(page, per_page, error_out=False)
    return jsonify({'data': [stat.as_dict() for stat in results.items], 'total': results.total})




