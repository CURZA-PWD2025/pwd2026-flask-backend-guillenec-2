from app.models import db
from app.models.user import User
from app.models.rol import Rol
from flask import jsonify, Response
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, create_refresh_token

class AuthController:
    @staticmethod
    def Register(request: dict) -> tuple[Response, int]:
        nombre = request.get("nombre")
        email = request.get("email")
        password = request.get("password")
        error = None

        if not nombre:
            error = "El nombre es requerido"
        if not email:
            error = "El email es requerido"
        if not password:
            error = "La contraseña es requerida"
        if error is None:
            try:
                rol_user = db.session.execute(
                    db.select(Rol).filter_by(nombre="user")
                ).scalar_one_or_none()
                if not rol_user:
                    return jsonify({"message": "No existe el rol base 'user'"}), 422

                user = User(
                    nombre=nombre, email=email, rol_id=rol_user.id, password=password
                )
                user.generate_password_hash(password)
                db.session.add(user)
                db.session.commit()
                return jsonify({"message": "usuario creado con exito"}), 201

            except IntegrityError:
                db.session.rollback()
                return jsonify({"message": "Usuario ya registrado"}), 409
        return jsonify({"message": error}), 422

    @staticmethod
    def Login(request: dict) -> tuple[Response, int]:
        email: str | None = request.get("email")
        password: str | None = request.get("password")

        error = None
        if not email:
            error = "El email es requerido"
        if not password:
            error = "La contraseña es requerida"

        if error is None:
            user = db.session.execute(
                db.select(User).filter_by(email=email)
            ).scalar_one_or_none()
            if user and user.validate_password(password):
                access_token = create_access_token(
                    identity=str(user.id),
                    additional_claims={"rol": user.rol.nombre if user.rol else None},
                )
                refresh_token = create_refresh_token(
                    identity=str(user.id),
                    additional_claims={"rol": user.rol.nombre if user.rol else None},
                )
                return jsonify(
                    {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "rol": user.rol.nombre if user.rol else None,
                        "nombre": user.nombre,
                    }
                ), 200
            return jsonify({"message": "Credenciales inválidas"}), 401

        return jsonify({"message": error}), 422
