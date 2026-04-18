from flask import Blueprint, request

from app.controllers.categoria_controller import CategoriaController


categorias = Blueprint("categorias", __name__, url_prefix="/categorias")


@categorias.route("/")
def get_all():
    return CategoriaController.get_all()


@categorias.route("/<int:id>")
def show(id: int):
    return CategoriaController.show(id)


@categorias.route("/", methods=["POST"])
def create():
    return CategoriaController.create(request.get_json() or {})


@categorias.route("/<int:id>", methods=["PUT"])
def update(id: int):
    return CategoriaController.update(request.get_json() or {}, id)


@categorias.route("/<int:id>", methods=["DELETE"])
def delete(id: int):
    return CategoriaController.delete(id)
