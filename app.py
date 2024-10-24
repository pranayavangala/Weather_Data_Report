from flask import Flask
from flask_migrate import Migrate
from Weather_app.models import db  # Assuming your db object is defined in models.py

app = Flask(__name__)
# Configure your database here (e.g., app.config['SQLALCHEMY_DATABASE_URI'] = ...)
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)
