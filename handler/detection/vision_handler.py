from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    jwt_required,
)
from flask import Blueprint, jsonify, request
from handler.detection.openai import open_ai
from handler.detection.gemini import gemini_ai

vision_bp = Blueprint('vision', __name__)
bcrypt = Bcrypt()

@vision_bp.route('/api/detection/gpt4', methods=['POST'])
@jwt_required()
def gpt4_vision():
    image_url = request.json.get('image_url', None)

    try:
        json_object = open_ai.generate_title_and_description(image_url=image_url)
        if json_object:
            return jsonify(json_object)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@vision_bp.route('/api/detection/gemini', methods=['POST'])
@jwt_required()
def gimini_vision():
    image_url = request.json.get('image_url', None)

    try:
        json_object = gemini_ai.generate_title_and_description(image_url=image_url)
        if json_object:
            return jsonify(json_object)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500