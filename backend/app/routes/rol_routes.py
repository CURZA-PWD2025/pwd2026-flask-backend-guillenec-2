from app.controllers.rol_controller import RolController
from flask import request, Blueprint

roles = Blueprint('roles', __name__, url_prefix='/roles')

@roles.route('/')
def get_all():
    return RolController.get_all()

@roles.route('/<int:id>')
def show(id):
    return RolController.show(id)

@roles.route("/", methods=['POST'])
def create():
    return RolController.create(request.get_json() or {}) 

@roles.route("/<int:id>", methods=['PUT'])
def update(id):
    return  RolController.update(request=request.get_json() or {}, id=id)
    

@roles.route("/<int:id>", methods=['DELETE'])
def destroy(id):
    return RolController.destroy( id)
