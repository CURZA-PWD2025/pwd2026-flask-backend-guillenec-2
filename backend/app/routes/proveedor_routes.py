from flask import Blueprint, request

from app.controllers.proveedor_controller import ProveedorController
from app.decorators.rol_access import rol_access
from flask_jwt_extended import jwt_required

proveedores = Blueprint("proveedores", __name__, url_prefix="/proveedores")

@proveedores.route("/")
@jwt_required()
@rol_access(['admin'])
def get_all():
    return ProveedorController.get_all()


@proveedores.route("/<int:id>")
@jwt_required()
@rol_access(['admin'])
def show(id: int):
    return ProveedorController.show(id)


@proveedores.route("/", methods=["POST"])
@jwt_required()
@rol_access(['admin'])
def create():
    return ProveedorController.create(request.get_json() or {})


@proveedores.route("/<int:id>", methods=["PUT"])
@jwt_required()
@rol_access(['admin'])
def update(id: int):
    return ProveedorController.update(request.get_json() or {}, id)


@proveedores.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@rol_access(['admin'])
def delete(id: int):
    return ProveedorController.delete(id)
