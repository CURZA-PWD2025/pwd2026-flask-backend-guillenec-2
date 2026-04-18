from flask import Blueprint, request

from app.controllers.proveedor_controller import ProveedorController


proveedores = Blueprint("proveedores", __name__, url_prefix="/proveedores")


@proveedores.route("/")
def get_all():
    return ProveedorController.get_all()


@proveedores.route("/<int:id>")
def show(id: int):
    return ProveedorController.show(id)


@proveedores.route("/", methods=["POST"])
def create():
    return ProveedorController.create(request.get_json() or {})


@proveedores.route("/<int:id>", methods=["PUT"])
def update(id: int):
    return ProveedorController.update(request.get_json() or {}, id)


@proveedores.route("/<int:id>", methods=["DELETE"])
def delete(id: int):
    return ProveedorController.delete(id)
