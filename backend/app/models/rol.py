from app.models.base_model import BaseModel
from app.models import db

class Rol(BaseModel):
    __tablename__="roles"
    nombre = db.Column(db.String, unique = True)
    users = db.relationship("User", back_populates="rol")

    def __init__(self, nombre) -> None:
        self.nombre = nombre
        
    def to_dict(self, include_users: bool = True):
        data: dict = super().to_dict()  # Obtener los campos de BaseModel
        data.update({
            "nombre": self.nombre,
        })
        if include_users:
            data["users"] = [user.to_dict(include_rol=False) for user in self.users]
        return data
    