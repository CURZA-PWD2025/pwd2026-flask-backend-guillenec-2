from flask import Blueprint, request

from app.controllers.categoria_controller import CategoriaController
from flask_jwt_extended import jwt_required
from app.decorators.rol_access import rol_access

categorias = Blueprint("categorias", __name__, url_prefix="/categorias")


@categorias.route("/")
@jwt_required()
def get_all():
    return CategoriaController.get_all()


@categorias.route("/<int:id>")
@jwt_required()
def show(id: int):
    return CategoriaController.show(id)


@categorias.route("/", methods=["POST"])
@jwt_required()
@rol_access(['admin'])
def create():
    return CategoriaController.create(request.get_json() or {})


@categorias.route("/<int:id>", methods=["PUT"])
@jwt_required()
@rol_access(['admin'])
def update(id: int):
    return CategoriaController.update(request.get_json() or {}, id)


@categorias.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@rol_access(['admin'])
def delete(id: int):
    return CategoriaController.delete(id)
