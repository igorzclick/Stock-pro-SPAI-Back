class SellerDomain:
    def __init__(self,name,cnpj,email,cellphone,password,status="Inativo"):
        self.name = name
        self.cnpj = cnpj
        self.email = email
        self.cellphone = cellphone
        self.password = password
        self.status = status
        
    def to_dict(self):
        return {
            "name": self.name,
            "cnpj": self.cnpj,
            "email": self.email,
            "cellphone": self.cellphone,
            "password": self.password,
            "status": self.status
        }