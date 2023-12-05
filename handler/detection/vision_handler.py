from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from flask import Blueprint, jsonify, request
from datetime import datetime
from handler.query_helpers import execute_query
import open_ai

vision_bp = Blueprint('vision', __name__)
bcrypt = Bcrypt()

@vision_bp.route('/api/detection', methods=['POST'])
@jwt_required()
def generate_title_and_description():
    image_r = request.json

    try:
        json_object = open_ai.generate_title_and_description(image_url=image_r['image_url'])
        if json_object:
            return jsonify(json_object)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500