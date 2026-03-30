from flask import request, jsonify, make_response
from src.Application.Service.user_service import UserService

class UserController:
    @staticmethod
    def register_user():
        data = request.get_json()
        nome = data.get('nome')
        email = data.get('email')
        password = data.get('password')

        user_required_fields=['nome','email','password']
        for field in user_required_fields:
            if not data.get(field):
                return  make_response(
                    jsonify({'error:' f'{field} is required '}),
                    400
                )

        

        user = UserService.create_user(nome, email, password)
        return make_response(jsonify({
            "mensagem": "User salvo com sucesso",
            "usuarios": user.to_dict()
        }), 200)
