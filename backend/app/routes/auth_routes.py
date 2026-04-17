from flask import Blueprint, request
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    return AuthController.Register(data)    

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    return AuthController.Login(data)

