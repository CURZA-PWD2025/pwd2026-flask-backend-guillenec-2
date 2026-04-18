from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError

from app.controllers import Controller
from app.models import db
from app.models.proveedor import Proveedor

class ProveedorController(Controller):
    @staticmethod
    def get_all() -> tuple[Response, int]:
        proveedores_list = (
            db.session.execute(db.select(Proveedor).order_by(db.desc(Proveedor.id)))
            .scalars()
            .all()
        )
        if len(proveedores_list) > 0:
            proveedores_to_dict = [proveedor.to_dict() for proveedor in proveedores_list]
            return jsonify(proveedores_to_dict), 200
        return jsonify({"message": "datos no encontrados"}), 404

    @staticmethod
    def show(id: int) -> tuple[Response, int]:
        proveedor = db.session.get(Proveedor, id)
        if proveedor:
            return jsonify(proveedor.to_dict()), 200

        return jsonify({"message": "proveedor no encontrado"}), 404
    
    @staticmethod
    def create(request: dict) -> tuple[Response, int]:
        nombre = request.get("nombre")
        contacto = request.get("contacto")
        telefono = request.get("telefono")
        email = request.get("email")
        error = None
        if not nombre:
            error = "El nombre es requerido"
        if not contacto:
            error = "El contacto es requerido"
        if not telefono:
            error = "El telefono es requerido"
        if not email:
            error = "El email es requerido"
        if error is None:
            try:
                proveedor = Proveedor(
                    nombre=nombre,
                    contacto=contacto,
                    telefono=telefono,
                    email=email,
                )
                db.session.add(proveedor)
                db.session.commit()
                return jsonify({"message": "proveedor creado con exito"}), 201
            except IntegrityError:
                db.session.rollback()
                return jsonify({"message": "Proveedor ya registrado"}), 409
        return jsonify({"message": error}), 422
    
    @staticmethod
    def update(request: dict, id: int) -> tuple[Response, int]:
        nombre = request.get("nombre")
        contacto = request.get("contacto")
        telefono = request.get("telefono")
        email = request.get("email")
    
        error = None
        if not nombre:
            error = "El nombre es requerido"
        if not contacto:
            error = "El contacto es requerido"
        if not telefono:
            error = "El telefono es requerido"
        if not email:
            error = "El email es requerido"
        if error is None:
            proveedor = db.session.get(Proveedor, id)
            if proveedor:
                try:
                    proveedor.nombre = nombre
                    proveedor.contacto = contacto
                    proveedor.telefono = telefono
                    proveedor.email = email
                    db.session.commit()
                    return jsonify({"message": "proveedor modificado con exito"}), 200
                except IntegrityError:
                    db.session.rollback()
                    return jsonify({"message": "Proveedor ya registrado"}), 409
            return jsonify({"message": "proveedor no encontrado"}), 404
        return jsonify({"message": error}), 422
    
    @staticmethod
    def delete(id: int) -> tuple[Response, int]:
        proveedor = db.session.get(Proveedor, id)
        if proveedor:
            if len(proveedor.productos) > 0:
                return jsonify({"message": "No se puede eliminar el proveedor porque tiene productos asociados"}), 409
            db.session.delete(proveedor)
            db.session.commit()
            return jsonify({"message": "proveedor eliminado con exito"}), 200
        return jsonify({"message": "proveedor no encontrado"}), 404
