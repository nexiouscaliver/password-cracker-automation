# app.py
from flask import Flask
from flask_restful import Api
from api.routes import initialize_routes
from config import Config
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Setup rate limiting (e.g., 200 per day and 50 per hour)
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )

    api = Api(app)
    initialize_routes(api)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=app.config.get("DEBUG", False))
