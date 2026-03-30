from flask import jsonify, make_response
from src.Application.Service.seller_service import SellerService
from src.Infrastructure.Model.seller_model import Seller
from src.Domain.seller import SellerDomain

class SellerController:
    @staticmethod
    def register_seller(body):
        seller = SellerDomain(
            name = body['name'],
            cnpj = body['cnpj'],
            email = body['email'],
            cellphone = body['cellphone'],
            password = body['password']
        )

        created_seller, error_message = SellerService.create_seller(seller)

        if error_message:
            return make_response(jsonify({"message": error_message}), 400)

        return make_response(jsonify({
                "message": "Seller registered successfully",
                "seller": created_seller.to_dict()
            }), 201)

    @staticmethod
    def get_all_sellers():
        sellers = SellerService.get_all_sellers()
        if sellers is None:
            return make_response(jsonify({"message": "Could not retrieve sellers"}), 500)
        return make_response(jsonify({
            "sellers": sellers
        }), 200)

    @staticmethod
    def get_seller_by_id(seller_id):
            
            seller = SellerService.get_seller_by_id(seller_id)
            if not seller:
                return make_response(jsonify({"message": "Seller not found"}), 404)
            return make_response(jsonify({
                "seller": seller
            }), 200)

    @staticmethod
    def update_seller(body, seller_id):
        seller_domain = SellerDomain(
            name=body.get('name'),
            cnpj=body.get('cnpj'),
            email=body.get('email'),
            cellphone=body.get('cellphone'),
            password=body.get('password')
        )

        seller, error_message = SellerService.update_seller(seller_id, seller_domain)

        if error_message:
            return make_response(jsonify({"message": error_message}), 400)

        if not seller:
            return make_response(jsonify({"message": "Seller not found or update failed"}), 404)

        return make_response(jsonify({
            "message": "Seller updated successfully",
            "seller": seller.to_dict()
        }), 200)

    @staticmethod
    def delete_seller(seller_id):
        seller, message = SellerService.delete_seller(seller_id)
        if not seller:
            return make_response(jsonify({"message": message}), 404)

        return make_response(jsonify({
            "message": message,
        }), 200)
    
    @staticmethod
    def activate_seller(cellphone, code):
        seller, error_message = SellerService.activate_seller(cellphone, code)
        
        if error_message:
            return make_response(jsonify({"message": error_message}), 400)
        
        if not seller:
            return make_response(jsonify({"message": "Seller not found"}), 404)
        
        return make_response(jsonify({
            "message": "Seller activated successfully",
            "seller": seller.to_dict()
        }), 200)
    
    @staticmethod
    def activate_seller(cellphone, code):
        seller, error_message = SellerService.activate_seller(cellphone, code)
        
        if error_message:
            return make_response(jsonify({"message": error_message}), 400)
        
        if not seller:
            return make_response(jsonify({"message": "Seller not found"}), 404)
        
        return make_response(jsonify({
            "message": "Seller activated successfully",
            "seller": seller.to_dict()
        }), 200)