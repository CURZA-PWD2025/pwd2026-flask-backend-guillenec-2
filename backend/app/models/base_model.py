from app.models import db

class BaseModel(db.Model):
    __abstract__ = True  # Esta clase no se mapeara a una tabla en la base de datos
    id = db.Column(db.Integer, primary_key=True)
    activo = db.Column(db.String(1), server_default="S")
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def to_dict(self): # Método para convertir el modelo a un diccionario
        return {
            "id": self.id,
            "activo": self.activo,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
