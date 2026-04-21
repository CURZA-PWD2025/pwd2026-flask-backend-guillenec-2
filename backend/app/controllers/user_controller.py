from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError

from app.controllers import Controller
from app.models import db
from app.models.user import User


class UserController(Controller):
    @staticmethod
    def get_all() -> tuple[Response, int]:
        users_list = (
            db.session.execute(db.select(User).order_by(db.desc(User.id)))
            .scalars()
            .all()
        )
        if len(users_list) > 0:
            users_to_dict = [user.to_dict() for user in users_list]
            return jsonify(users_to_dict), 200
        return jsonify({"message": "datos no encontrados"}), 404

    @staticmethod
    def show(id: int) -> tuple[Response, int]:
        user = db.session.get(User, id)
        if user:
            return jsonify(user.to_dict()), 200

        return jsonify({"message": "usuario no encontrado"}), 404

    @staticmethod
    def create(request: dict) -> tuple[Response, int]:
        nombre = request.get("nombre")
        email = request.get("email")
        password = request.get("password")
        rol_id = request.get("rol_id", 1)
        error = None
        if not nombre:
            error = "El nombre es requerido"
        if not email:
            error = "El email es requerido"
        if not password:
            error = "La contraseña es requerida"
        if error is None:
            try:
                user = User(
                    nombre=nombre, email=email, password=password, rol_id=int(rol_id)
                )
                user.generate_password_hash(password)
                db.session.add(user)
                db.session.commit()
                return jsonify({"message": "usuario creado con exito"}), 201
            except ValueError:
                return jsonify({"message": "rol_id debe ser numerico"}), 422
            except IntegrityError:
                db.session.rollback()
                return jsonify({"message": "Usuario ya registrado"}), 409
        return jsonify({"message": error}), 422

    @staticmethod
    def update(request, id) -> tuple[Response, int]:
        nombre = request.get("nombre")
        email = request.get("email")
        error = None
        if not nombre:
            error = "El nombre es requerido"
        if not email:
            error = "El email es requerido"
        if error is None:
            user = db.session.get(User, id)
            if user:
                try:
                    user.nombre = nombre
                    user.email = email
                    db.session.commit()
                    return jsonify({"message": "usuario modificado con exito"}), 200
                except IntegrityError:
                    error = "el email o el username ya existen"
                    return jsonify({"message": error}), 409
            else:
                error = "usuario no encontrado"

        return jsonify({"message": error}), 404

    @staticmethod
    def destroy(id: int) -> tuple[Response, int]:
        user = db.session.get(User, id)
        error = None
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "el usuario fue eliminado con exito"}), 200
        else:
            error = "usuario no encontrado"
        return jsonify({"message": error}), 404
