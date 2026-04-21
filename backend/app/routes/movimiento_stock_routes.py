from flask import Blueprint, request

from app.controllers.movimiento_stock_controller import MovimientoStockController
from flask_jwt_extended import (get_jwt_identity)

from flask_jwt_extended import jwt_required
from app.decorators.rol_access import rol_access

movimientos_stock = Blueprint(
    "movimientos_stock", __name__, url_prefix="/movimientos"
)

# Rutas Practico
@movimientos_stock.route("/")
@jwt_required()
@rol_access(['admin'])
def get_all():
    return MovimientoStockController.get_all()

@movimientos_stock.route("/mis")
@jwt_required()
def get_by_user_id():
    return MovimientoStockController.get_by_user_id(get_jwt_identity())

@movimientos_stock.route("/", methods=["POST"])
@jwt_required()
def create():
    return MovimientoStockController.create(request.get_json() or {}, get_jwt_identity())

# Rutas adicionales 
@movimientos_stock.route("/<int:id>", methods=["PUT"])
@jwt_required()
@rol_access(['admin'])
def update(id: int):
    return MovimientoStockController.update(id, request.get_json() or {})

@movimientos_stock.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@rol_access(['admin'])
def delete(id: int):
    return MovimientoStockController.delete(id)
