from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError

from app.controllers import Controller
from app.models import db
from app.models.categoria import Categoria
from flask_jwt_extended import jwt_required
from app.decorators.rol_access import rol_access

class CategoriaController(Controller):
    @staticmethod
    @jwt_required()
    def get_all() -> tuple[Response, int]:
        categorias_list = (
            db.session.execute(db.select(Categoria).order_by(db.desc(Categoria.id)))
            .scalars()
            .all()
        )
        if len(categorias_list) > 0:
            categorias_to_dict = [categoria.to_dict() for categoria in categorias_list]
            return jsonify(categorias_to_dict), 200
        return jsonify({"message": "datos no encontrados"}), 404

    @staticmethod
    @jwt_required()
    def show(id: int) -> tuple[Response, int]:
        categoria = db.session.get(Categoria, id)
        if categoria:
            return jsonify(categoria.to_dict()), 200

        return jsonify({"message": "categoria no encontrada"}), 404

    @staticmethod
    @jwt_required()
    @rol_access(['admin'])
    def create(request: dict) -> tuple[Response, int]:
        nombre = request.get("nombre")
        descripcion = request.get("descripcion")
        error = None
        if not nombre:
            error = "El nombre es requerido"
        if not descripcion:
            error = "La descripcion es requerida"
        if error is None:
            try:
                categoria = Categoria(nombre=nombre, descripcion=descripcion)
                db.session.add(categoria)
                db.session.commit()
                return jsonify({"message": "categoria creada con exito"}), 201
            except IntegrityError:
                db.session.rollback()
                return jsonify({"message": "Categoria ya registrada"}), 409
        return jsonify({"message": error}), 422
    
    @staticmethod
    @jwt_required()
    @rol_access(['admin'])
    def update(request: dict, id: int) -> tuple[Response, int]:
        nombre = request.get("nombre")
        descripcion = request.get("descripcion")
        if not nombre:
            return jsonify({"message": "El nombre es requerido"}), 422
        if not descripcion:
            return jsonify({"message": "La descripcion es requerida"}), 422

        categoria = db.session.get(Categoria, id)
        if not categoria:
            return jsonify({"message": "categoria no encontrada"}), 404

        try:
            categoria.nombre = nombre
            categoria.descripcion = descripcion
            db.session.commit()
            return jsonify({"message": "categoria modificada con exito"}), 200
        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "Nombre de categoria en uso"}), 409
    
    @staticmethod
    @jwt_required()
    @rol_access(['admin'])
    def delete(id: int) -> tuple[Response, int]:
        categoria = db.session.get(Categoria, id)
        if categoria:
            if len(categoria.productos) > 0:
                return jsonify({"message": "No se puede eliminar la categoria porque tiene productos asociados"}), 409
            try:
                db.session.delete(categoria)
                db.session.commit()
                return jsonify({"message": "categoria eliminada con exito"}), 200
            except IntegrityError:
                db.session.rollback()
                return jsonify({"message": "No se puede eliminar categoria, esta siendo usada"}), 409
        return jsonify({"message": "categoria no encontrada"}), 404
