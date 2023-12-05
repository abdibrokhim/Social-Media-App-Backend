import os
import json
import logging.config
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import JWTManager
import structlog
from dotenv import load_dotenv, find_dotenv
from flask import Flask, jsonify
from flask import Response
from flask_cors import CORS
from prometheus_client import CONTENT_TYPE_LATEST
from prometheus_client import CollectorRegistry
from prometheus_client import generate_latest
from prometheus_client import multiprocess
from config.logger import (
    prepare_logging_config
)
from service.constants import (
    APP_LOG_LEVEL_ENV_KEY,
    SERVER_LOG_LEVEL_ENV_KEY,
    API_ERROR_UNHANDELED,
)
from helper.api_types import create_error_return
from handler.user import user_handler
from handler.post import post_handler
from handler.category import category_handler
from handler.auth import auth_handler
from handler.detection import vision_handler
from handler.filters import user_filter
from handler.filters import post_filter
from handler.auth.auth_handler import get_revoked_token
from handler.user.user_handler import get_user_by_username


def setup_logging():
    """
      Setup logging with struct log
      :return:
      """
    log_level = os.getenv(APP_LOG_LEVEL_ENV_KEY)
    logging.config.dictConfig(
        prepare_logging_config(
            int(log_level) if log_level is not None else logging.INFO
        )
    )


def init_app(use_log_handlers="gunicorn.error") -> Flask:
    """
      Init application
      :returns Flask
      """
    server_log_level = os.getenv(SERVER_LOG_LEVEL_ENV_KEY)
    flask_app = Flask(__name__)
    requested_logger = logging.getLogger(use_log_handlers)
    flask_app.logger.handlers = requested_logger.handlers[:]
    werkzeug_logger = logging.getLogger("werkzeug")
    werkzeug_logger.setLevel(
        int(server_log_level) if server_log_level is not None else logging.ERROR
    )
    log = structlog.get_logger()

    log.info(
        "the flask application was initialized",
        server_log_level=werkzeug_logger.level,
        app_log_level=logging.root.level,
    )

        
    return flask_app


load_dotenv(find_dotenv())

setup_logging()
app = init_app()
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-string')
jwt = JWTManager(app)
cors = CORS(app)

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_headers, jwt_data):
    identity = jwt_data["sub"]
    return get_user_by_username(identity)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({"message": "Token has expired", "error": "token_expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"message": "Signature verification failed", "error": "invalid_token"}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"message": "Request doesn't contain a valid token", "error": "authorization_required"}), 401

@jwt.token_in_blocklist_loader
def token_in_blocklist_callback(jwt_header, jwt_data):
    jti = jwt_data['jti']
    token = get_revoked_token(jti)
    return token is not None

@app.errorhandler(HTTPException)
def handle_bad_request(error: Exception) -> Response:
    log = structlog.get_logger()
    log.error(error)
    return Response(
        response=json.dumps(
            create_error_return(
                API_ERROR_UNHANDELED,
                "there was unknown error. please get in touch with the support",
            )
        ),
        status=400,
        mimetype="application/json",
    )


@app.route("/metrics")
def metrics():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    data = generate_latest(registry)
    return Response(data, mimetype=CONTENT_TYPE_LATEST)


app.register_blueprint(auth_handler.auth_bp)
app.register_blueprint(user_handler.user_bp)
app.register_blueprint(post_handler.post_bp)
app.register_blueprint(category_handler.category_bp)
app.register_blueprint(vision_handler.vision_bp)
app.register_blueprint(user_filter.user_filter_bp)
app.register_blueprint(post_filter.post_filter_bp)
app.register_error_handler(400, handle_bad_request)

