from src.config.data_base import db

class Seller_code(db.Model):
    __tablename__ = 'seller_codes'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)
    
def to_dict(self):
    return {
        "id": self.id,
        "code": self.code
}    
    