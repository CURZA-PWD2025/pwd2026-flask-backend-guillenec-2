from flask import Blueprint, request
from app.controllers.auth_controller import AuthController
from flask_jwt_extended import jwt_required
from app.decorators.rol_access import rol_access

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    return AuthController.Register(data)    

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    return AuthController.Login(data)

@jwt_required()
@rol_access(['admin', 'operador'])
@auth_bp.route('/me', methods=['GET'])
def me():
    return AuthController.GetMe()
