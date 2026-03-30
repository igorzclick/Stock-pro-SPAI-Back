from src.config.data_base import db

class Seller(db.Model):
    __tablename__ = 'sellers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cnpj= db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    cellphone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default="Inativo")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cnpj": self.cnpj,
            "email": self.email,
            "cellphone": self.cellphone,
            "password": self.password,
            "status": self.status,
            "deleted_at": self.deleted_at
        }