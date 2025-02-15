from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from kafka import KafkaProducer
from json import dumps

from datetime import datetime

db = SQLAlchemy()

app = Flask(__name__)

def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes
    from app.misc import log


    app.config.from_object(config_by_name[env or "test"])
    api = Api(app, title="UdaConnect API", version="0.1.0")

    CORS(app)  # Set CORS for development

    register_routes(api, app)
    db.init_app(app)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app

