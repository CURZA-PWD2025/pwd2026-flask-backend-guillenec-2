from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError

from app.controllers import Controller
from app.models import db
from app.models.rol import Rol


class RolController(Controller):
    @staticmethod
    def get_all() -> tuple[Response, int]:
        roles_list = (
            db.session.execute(db.select(Rol).order_by(db.desc(Rol.id))).scalars().all()
        )
        
        if roles_list:
            roles_to_dict = [rol.to_dict() for rol in roles_list]
            return jsonify(roles_to_dict), 200

        return jsonify({"message": "datos no encontrados"}), 404

    @staticmethod
    def show(id: int) -> tuple[Response, int]:
        rol = db.session.get(Rol, id)
        if rol:
            return jsonify(rol.to_dict()), 200
        return jsonify({"message": "rol no encontrado"}), 404

    @staticmethod
    def create(request: dict) -> tuple[Response, int]:
        nombre = request.get("nombre")

        if not nombre:
            return jsonify({"message": "El nombre es requerido"}), 422

        try:
            rol = Rol(nombre=nombre)
            db.session.add(rol)
            db.session.commit()
            return jsonify({"message": "rol creado con exito"}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "rol ya registrado"}), 409

    @staticmethod
    def update(request: dict, id: int) -> tuple[Response, int]:
        nombre = request.get("nombre")

        if not nombre:
            return jsonify({"message": "El nombre es requerido"}), 422

        rol = db.session.get(Rol, id)
        if not rol:
            return jsonify({"message": "rol no encontrado"}), 404

        try:
            rol.nombre = nombre
            db.session.commit()
            return jsonify({"message": "rol modificado con exito"}), 200
        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "el nombre ya existe"}), 409

    @staticmethod
    def destroy(id: int) -> tuple[Response, int]:
        rol = db.session.get(Rol, id)
        if not rol:
            return jsonify({"message": "rol no encontrado"}), 404

        db.session.delete(rol)
        db.session.commit()
        return jsonify({"message": "el rol fue eliminado con exito"}), 200
