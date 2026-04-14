class ProductDomain:
    def __init__(self, seller_id, name, price, quantity, img, status="Inativo"):
        self.seller_id = seller_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.status = status
        self.img = img
        
    def to_dict(self):
        return {
            "seller_id": self.seller_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "status": self.status,
            "img": self.img
        }