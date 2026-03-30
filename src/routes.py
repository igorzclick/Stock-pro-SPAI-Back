from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask import jsonify, make_response, request

from src.Application.Controllers.auth_controller import AuthController
from src.Application.Controllers.seller_controller import SellerController
from src.Application.Controllers.user_controller import UserController
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
