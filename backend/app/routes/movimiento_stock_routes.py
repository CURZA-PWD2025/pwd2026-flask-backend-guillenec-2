from flask import Blueprint, request

from app.controllers.movimiento_stock_controller import MovimientoStockController
from flask_jwt_extended import (get_jwt_identity)

movimientos_stock = Blueprint(
    "movimientos_stock", __name__, url_prefix="/movimientos"
)

# Rutas Practico
@movimientos_stock.route("/")
def get_all():
    return MovimientoStockController.get_all()

@movimientos_stock.route("/mis")
def get_by_current_user():
    return MovimientoStockController.get_by_user_id(get_jwt_identity())

@movimientos_stock.route("/", methods=["POST"])
def create():
    return MovimientoStockController.create(request.get_json() or {})

# Rutas adicionales 
@movimientos_stock.route("/<int:id>")
def get_by_id(id: int):
    return MovimientoStockController.get_by_id(id)

@movimientos_stock.route("/<int:id>", methods=["PUT"])
def update(id: int):
    return MovimientoStockController.update(id, request.get_json() or {})


@movimientos_stock.route("/<int:id>", methods=["DELETE"])
def delete(id: int):
    return MovimientoStockController.delete(id)


@movimientos_stock.route("/producto/<int:producto_id>")
def get_by_producto_id(producto_id: int):
    return MovimientoStockController.get_by_producto_id(producto_id)


@movimientos_stock.route("/usuario/<int:user_id>")
def get_by_user_id(user_id: int):
    return MovimientoStockController.get_by_user_id(user_id)
