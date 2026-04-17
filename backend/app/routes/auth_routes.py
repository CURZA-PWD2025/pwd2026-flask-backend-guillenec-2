from flask import Blueprint, request
from app.controllers.auth_controller import AuthController
from flask_jwt_extended import jwt_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    return AuthController.register(data)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    return AuthController.login(data)


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    return AuthController.get_me()
