from src.Infrastructure.Model.product_model import Product
from src.config.data_base import db
from src.Domain.product import ProductDomain
from flask_jwt_extended import get_jwt_identity

class ProductService:
    @staticmethod
    def create_product(new_product):
        try:
            if Product.query.filter_by(name = new_product.name).first():
                return None, "Product already exists"
                    
            product = Product(
                seller_id = new_product.seller_id,
                name = new_product.name,
                price = new_product.price,
                quantity = new_product.quantity,
                img = new_product.img,
                status = "Ativo"
            )

            db.session.add(product)
            db.session.commit()
            return product, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
        
    @staticmethod
    def get_all_products():
        try:
            products = Product.query.all()
            return [product.to_dict() for product in products]
        except Exception as e:
            return None
        
    @staticmethod
    def get_product_by_id(product_id):
        try:
            product = Product.query.filter_by(id=product_id).first()
            return product.to_dict()
        except Exception as e:
            return None
        
    @staticmethod
    def update_product(product_id, product_domain):
        try:
            product = Product.query.filter_by(id=product_id).first()
            if not product:
                return None, "Product not found"

            product.name = product_domain.name
            product.price = product_domain.price
            product.quantity = product_domain.quantity
            product.img = product_domain.img
            
            if product_domain.quantity == 0:
                product.status = "Inativo"
            else:
                product.status = product_domain.status

            db.session.commit()
            return product, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)
        
    @staticmethod
    def delete_product(product_id):
        try:
            product = Product.query.filter_by(id=product_id).first()

            if not product:
                return None, "Product not found"
            
            db.session.delete(product)
            db.session.commit()
            return True, "Product deleted successfully"
        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    @staticmethod
    def get_low_stock_products(limit: int = 5, threshold: int = 10):
        try:
            products = (
                Product.query
                .filter(Product.quantity < threshold)
                .order_by(Product.quantity.asc())
                .limit(limit)
                .all()
            )
            return [product.to_dict() for product in products]
        except Exception:
            return []