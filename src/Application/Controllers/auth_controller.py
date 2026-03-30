from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt
from src.Infrastructure.Model.seller_model import Seller
from src.config.data_base import db
from src.config.jwt_config import JWTConfig
from flask_jwt_extended import create_access_token, create_refresh_token

class AuthController:
    @staticmethod
    def login():
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return make_response(jsonify({"message": "Email and password are required"}), 400)

        seller = Seller.query.filter_by(email=email).first()

        if not seller or seller.password != password:
            return make_response(jsonify({"message": "Invalid credentials"}), 401)

        if getattr(seller, "status", "Inativo") != "Ativo":
            return make_response(jsonify({"message": "Seller not active"}), 403)

        access_token = create_access_token(identity=str(seller.id))
        refresh_token = create_refresh_token(identity=str(seller.id))

        return make_response(jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token 
        }), 200)
    
    @staticmethod
    def logout():
        try:
            jti = get_jwt()['jti']
            
            JWTConfig.revoke_token(jti)
            
            return make_response(jsonify({
                "message": "Logout successful. Token has been revoked."
            }), 200)
        except Exception as e:
            return make_response(jsonify({
                "message": "Error during logout",
                "error": str(e)
            }), 500)