from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask import jsonify, make_response, request

from src.Application.Controllers.auth_controller import AuthController
from src.Application.Controllers.seller_controller import SellerController
from src.Application.Controllers.user_controller import UserController
from src.Application.Controllers.product_controller import ProductController
from src.Application.Dto.seller_dto import SellerRegisterSchema
from src.config.data_base import db

def init_routes(app):
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up"}), 200)

    @app.route('/user', methods=['POST'])
    def register_user():
        return UserController.register_user()

    @app.route('/auth/login', methods=['POST'])
    def login():
        return AuthController.login()

    @app.route('/auth/logout', methods=['POST'])
    @jwt_required()
    def logout():
        return AuthController.logout()

    @app.route('/seller/register', methods=['POST'])
    def register_seller():
        data = request.get_json()
        errors = SellerRegisterSchema().validate(data)
        if errors:
            return make_response(jsonify(errors), 400)
        return SellerController.register_seller(data)

    @app.route("/auth/refresh", methods=["POST"])
    @jwt_required(refresh=True)
    def refresh():
        return jsonify(access_token=create_access_token(identity=str(get_jwt_identity())))

    @app.route("/seller/activate", methods=["POST"])
    def activate_seller():
        data = request.get_json()
        cellphone = data.get("cellphone")
        code = data.get("code")

        if not cellphone or not code:
            return make_response(jsonify({"message": "cellphone and code are required"}), 400)

        return SellerController.activate_seller(cellphone, code)

    @app.route("/product", methods=['POST'])
    @jwt_required()
    def create_product():
        user_id = get_jwt_identity()
        if not user_id:
            return make_response(jsonify({"message": "Access denied. You must be logged in to create a product."}), 403)
        data = request.get_json()
        return ProductController.create_product(data)
    
    @app.route("/product", methods=['GET'])
    @jwt_required()
    def get_all_products():
        user_id = get_jwt_identity()
        if not user_id:
            return make_response(jsonify({"message": "Access denied. You must be logged in to retrieve products."}), 403)
        return ProductController.get_all_products()

    @app.route("/product/<int:product_id>", methods=['GET'])
    @jwt_required()
    def get_product_by_id(product_id):
        user_id = get_jwt_identity()
        if not user_id:
            return make_response(jsonify({"message": "Access denied. You must be logged in to retrieve products."}), 403)
        return ProductController.get_product_by_id(product_id)
    
    @app.route("/product/<int:product_id>", methods=['PUT'])
    @jwt_required()
    def update_product(product_id):
        user_id = get_jwt_identity()
        if not user_id:
            return make_response(jsonify({"message": "Access denied. You must be logged in to update a product."}), 403)
        data = request.get_json()
        return ProductController.update_product(data, product_id)
    
    @app.route("/product/<int:product_id>", methods=['DELETE'])
    @jwt_required()
    def delete_product(product_id):
        user_id = get_jwt_identity()
        if not user_id:
            return make_response(jsonify({"message": "Access denied. You must be logged in to delete a product."}), 403)
        return ProductController.delete_product(product_id)