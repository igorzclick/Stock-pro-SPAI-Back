import random
from src.Infrastructure.http.whatsapp import send_whatsapp_message 
from src.Infrastructure.Model.seller_code_model import Seller_code
from src.Domain.seller import SellerDomain
from src.Infrastructure.Model.seller_model import Seller
from src.config.data_base import db
from datetime import datetime

class SellerService:
    @staticmethod
    def create_seller(new_seller):
        try:
            if Seller.query.filter_by(email=new_seller.email).first():
                return None, "Email already registered"
            if Seller.query.filter_by(cnpj=new_seller.cnpj).first():
                return None, "CNPJ already registered"
            if Seller.query.filter_by(cellphone=new_seller.cellphone).first():
                return None, "Cellphone already registered"
            
            seller = Seller(
                name=new_seller.name,
                cnpj=new_seller.cnpj,
                email=new_seller.email,
                cellphone=new_seller.cellphone,
                password=new_seller.password
            )

            db.session.add(seller)
            db.session.commit()

            code = str(random.randint(1000, 9999))

            seller_code = Seller_code(code=code, seller_id=seller.id)
            db.session.add(seller_code)
            db.session.commit()

            send_whatsapp_message(new_seller.cellphone, code)
            
            return seller, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def get_all_sellers():
        try:
            sellers = Seller.query.filter_by(deleted_at=None).all()        
            return [seller.to_dict() for seller in sellers]
        except Exception as e:
            return None
            
    @staticmethod
    def get_seller_by_id(id):
        try:
            seller = Seller.query.filter_by(id=id, deleted_at=None).first()        
            return seller.to_dict()
        except Exception as e:
            return None
        
    @staticmethod
    def update_seller(id, update_seller):
        try:
            seller = Seller.query.filter_by(id=id).first()

            seller_by_email = Seller.query.filter_by(email=update_seller.email).first()
            if seller_by_email != None and seller_by_email.id != seller.id:
                return None, "Email already registered"
            seller_by_cpnj = Seller.query.filter_by(cnpj=update_seller.cnpj).first()
            if seller_by_cpnj != None and seller_by_cpnj.id != seller.id:
                return None, "CNPJ already registered"
            seller_by_cellphone = Seller.query.filter_by(cellphone=update_seller.cellphone).first()
            if seller_by_cellphone != None and seller_by_cellphone.id != seller.id:
                return None, "Cellphone already registered"

            if not seller:
                return None, "Seller not found"
            seller.name = update_seller.name
            seller.cnpj = update_seller.cnpj
            seller.email = update_seller.email
            seller.cellphone = update_seller.cellphone
            seller.password = update_seller.password
            
            db.session.commit()
            return seller, None
        
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)
         
    @staticmethod
    def delete_seller(seller_id):
        try:
            seller = Seller.query.filter_by(id=seller_id).first()
            if not seller:
                return None, "Seller not found"
            
            seller.deleted_at = datetime.utcnow()
            db.session.commit()
            return True, 'Seller deleted successfully'
        except Exception as e:
            return None
    
    @staticmethod
    def activate_seller(cellphone, code):
        try:
            seller = Seller.query.filter_by(cellphone=cellphone).first()
            if not seller:
                return None, "Seller not found"
            
            seller_code = Seller_code.query.filter_by(
                seller_id=seller.id, 
                code=code
            ).first()
            if not seller_code:
                return None, "Invalid code"
            
            seller.status = "Ativo"
            db.session.commit()
            
            return seller, None
        
        except Exception as e:
            db.session.rollback()
            return None, str(e)