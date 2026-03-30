from Infrastructure.Model.seller_model import Seller


class AuthService:
    @staticmethod
    def login(email, password):
        try:
            seller = Seller.query.filter_by(email=email).first()
            if getattr(seller, "status", "Inativo") != "Ativo":
                return None, "Seller not active"
            if not seller and seller.password != password:
                return None, "Invalid credentials"
            if not seller:
                return None, "Seller not found"
            if seller.password != password:
                return None, "Invalid password"
            return seller
        except Exception as e:
            return None, str(e)

