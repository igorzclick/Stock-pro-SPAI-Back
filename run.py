from apiflask import APIFlask
from src.config.data_base import init_db
from src.Application.Dto.seller_dto import SellerRegisterSchema
from src.Application.Service.seller_service import SellerService
from src.routes import init_routes
from src.config.jwt_config import JWTConfig
from flask_cors import CORS

def create_app():
    app = APIFlask(__name__)
    CORS(app, origins="*")
    app.config["JWT_SECRET_KEY"] = "grupinho_2.0"
    app.config["JWT_ALGORITHM"] = "HS256"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600
    app.config["JWT_IDENTITY_CLAIM"] = "sub"
    
    JWTConfig.initialize_jwt(app)

    init_db(app)

    init_routes(app)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')