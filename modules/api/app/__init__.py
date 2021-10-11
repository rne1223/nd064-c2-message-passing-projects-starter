from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from kafka import KafkaProducer
from json import dumps

from datetime import datetime

db = SQLAlchemy()

app = Flask(__name__)

@app.before_first_request
def kafkaSetup():
    # Set up a Kafka producer
    KAFKA_SERVER = 'kafka-0.kafka-headless.default.svc.cluster.local:9093'
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                           value_serializer=lambda x: dumps(x).encode('utf-8'),
                           api_version=(0,10,1))

    g.kafka_producer = producer

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

