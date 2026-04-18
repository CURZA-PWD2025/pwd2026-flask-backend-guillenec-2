from flask import Blueprint, request

from app.controllers.producto_controller import ProductoController


productos = Blueprint("productos", __name__, url_prefix="/productos")


@productos.route("/")
def get_all():
    return ProductoController.get_all()


@productos.route("/<int:id>")
def show(id: int):
    return ProductoController.show(id)


@productos.route("/", methods=["POST"])
def create():
    return ProductoController.create(request.get_json() or {})


@productos.route("/<int:id>", methods=["PUT"])
def update(id: int):
    return ProductoController.update(id, request.get_json() or {})


@productos.route("/<int:id>", methods=["DELETE"])
def delete(id: int):
    return ProductoController.delete(id)
