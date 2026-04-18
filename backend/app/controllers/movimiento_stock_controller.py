from flask import Response, jsonify
from sqlalchemy.exc import IntegrityError

from app.controllers import Controller
from app.models import db
from app.models.movimiento_stock import MovimientoStock
from app.models.producto import Producto
from app.models.user import User

from flask_jwt_extended import jwt_required
from app.decorators.rol_access import rol_access

class MovimientoStockController(Controller):
    @staticmethod
    @rol_access(['admin'])
    def get_all() -> tuple[Response, int]:
        try:
            movimientos = db.session.query(MovimientoStock).all()
            return jsonify([movimiento.to_dict() for movimiento in movimientos]), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "Error interno del servidor"}), 500

    @staticmethod
    @jwt_required()
    def get_by_id(id: int) -> tuple[Response, int]:
        try:
            movimiento = db.session.get(MovimientoStock, id)
            if not movimiento:
                return jsonify({"message": "Movimiento de stock no encontrado"}), 404
            return jsonify(movimiento.to_dict()), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "Error interno del servidor"}), 500

    @staticmethod
    @jwt_required()
    def get_by_producto_id(producto_id: int) -> tuple[Response, int]:
        try:
            movimientos = db.session.query(MovimientoStock).filter_by(producto_id=producto_id).all()
            if not movimientos:
                return jsonify({"message": "No se encontraron movimientos de stock para este producto"}), 404
            return jsonify([movimiento.to_dict() for movimiento in movimientos]), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "Error interno del servidor"}), 500

    @staticmethod
    def get_by_user_id(user_id: int) -> tuple[Response, int]:
        try:
            movimientos = db.session.query(MovimientoStock).filter_by(user_id=user_id).all()
            if not movimientos:
                return jsonify({"message": "No se encontraron movimientos de stock para este usuario"}), 404
            return jsonify([movimiento.to_dict() for movimiento in movimientos]), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "Error interno del servidor"}), 500


    @staticmethod
    def create(data: dict) -> tuple[Response, int]:
        try:
            tipo = data.get("tipo")
            cantidad = data.get("cantidad")
            motivo = data.get("motivo")
            producto_id = data.get("producto_id")
            user_id = data.get("user_id")

            if not tipo:
                return jsonify({"message": "El tipo es requerido"}), 422

            try:
                cantidad = int(cantidad)
            except (TypeError, ValueError):
                return jsonify({"message": "La cantidad es requerida y debe ser un numero entero"}), 422

            if not producto_id:
                return jsonify({"message": "El producto es requerido"}), 422
            if not user_id:
                return jsonify({"message": "El usuario es requerido"}), 422

            try:
                producto_id = int(producto_id)
                user_id = int(user_id)
            except (TypeError, ValueError):
                return jsonify({"message": "producto_id y user_id deben ser numericos"}), 422

            producto = db.session.get(Producto, producto_id)
            user = db.session.get(User, user_id)
            if not producto:
                return jsonify({"message": "Producto no encontrado"}), 404
            if not user:
                return jsonify({"message": "Usuario no encontrado"}), 404

            movimiento = MovimientoStock(
                tipo=tipo,
                cantidad=cantidad,
                motivo=motivo,
                producto_id=producto_id,
                user_id=user_id,
            )

            try:
                movimiento.validate_tipo()
            except ValueError as error:
                return jsonify({"message": str(error)}), 422

            if not movimiento.validate_cantidad():
                return jsonify({"message": "La cantidad debe ser mayor a cero"}), 422

            if tipo == "salida":
                if producto.stock_actual < cantidad:
                    return jsonify({"message": "No hay suficiente stock para realizar esta salida"}), 400
                producto.stock_actual -= cantidad
            else:
                producto.stock_actual += cantidad

            db.session.add(movimiento)
            db.session.commit()

            return jsonify({"message": "Movimiento de stock creado con éxito"}), 201

        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "Error de integridad en la base de datos"}), 409
        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify({"message": "Error interno del servidor"}), 500

    @staticmethod
    def delete(id: int) -> tuple[Response, int]:
        try:
            movimiento = db.session.get(MovimientoStock, id)
            if not movimiento:
                return jsonify({"message": "Movimiento de stock no encontrado"}), 404
            
            producto = db.session.get(Producto, movimiento.producto_id)
            if movimiento.tipo == "salida":
                producto.stock_actual += movimiento.cantidad
            else:
                if producto.stock_actual < movimiento.cantidad:
                    return jsonify({"message": "No hay suficiente stock para eliminar esta entrada"}), 400
                producto.stock_actual -= movimiento.cantidad

            db.session.delete(movimiento)
            db.session.commit()

            return jsonify({"message": "Movimiento de stock eliminado con éxito"}), 200

        except IntegrityError:
            db.session.rollback()
            return jsonify({"message": "Error de integridad en la base de datos"}), 409
        except Exception as e:
            db.session.rollback()
            print(e)
            return jsonify({"message": "Error interno del servidor"}), 500
        
    
