from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    jwt_required,
)
from flask import Blueprint, jsonify, request
from handler.detection import open_ai

vision_bp = Blueprint('vision', __name__)
bcrypt = Bcrypt()

@vision_bp.route('/api/detection', methods=['POST'])
@jwt_required()
def get_title_and_description():
    image_url = request.json.get('image_url', None)

    try:
        json_object = open_ai.generate_title_and_description(image_url=image_url)
        if json_object:
            return jsonify(json_object)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500