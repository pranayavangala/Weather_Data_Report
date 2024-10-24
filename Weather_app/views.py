from flask import Blueprint, jsonify, request
from models import WeatherData, WeatherStats

main = Blueprint('main', __name__)


@main.route('/api/weather', methods=['GET'])
def get_weather_data():
    """
    Get weather data for a specific station or all stations.
    ---
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: The page number of the results.
      - name: per_page
        in: query
        type: integer
        required: false
        default: 10
        description: Number of records per page.
      - name: station_id
        in: query
        type: string
        required: false
        description: Filter records by station ID.
    responses:
      200:
        description: A list of weather data records.
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  date:
                    type: string
                    format: date
                  station_id:
                    type: string
                  max_temperature:
                    type: number
                    format: float
                  min_temperature:
                    type: number
                    format: float
                  precipitation:
                    type: number
                    format: float
            total:
              type: integer
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    station_id = request.args.get('station_id', None)

    query = WeatherData.query
    if station_id:
        query = query.filter_by(station_id=station_id)

    results = query.paginate(page, per_page, error_out=False)
    return jsonify({
        'data': [record.as_dict() for record in results.items],
        'total': results.total
    })


@main.route('/api/weather/stats', methods=['GET'])
def get_weather_stats():
    """
    Get weather statistics.
    ---
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: The page number of the results.
      - name: per_page
        in: query
        type: integer
        required: false
        default: 10
        description: Number of records per page.
    responses:
      200:
        description: A list of weather statistics.
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  # Add other fields as needed for your WeatherStats model
            total:
              type: integer
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    results = WeatherStats.query.paginate(page, per_page, error_out=False)
    return jsonify({
        'data': [stat.as_dict() for stat in results.items],
        'total': results.total
    })
