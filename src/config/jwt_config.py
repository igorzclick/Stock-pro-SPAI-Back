import os
from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask import current_app

class JWTConfig:
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret")
    ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 24))
    )
    REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 7))
    )
    
    blacklisted_tokens = set()
    
    @staticmethod
    def initialize_jwt(app):
        jwt = JWTManager(app)
        
        @jwt.token_in_blocklist_loader
        def check_if_token_revoked(jwt_header, jwt_payload):
            return jwt_payload['jti'] in JWTConfig.blacklisted_tokens
        
        @jwt.revoked_token_loader
        def revoked_token_callback(jwt_header, jwt_payload):
            return {"message": "The token has been revoked."}, 401
    
    @staticmethod
    def revoke_token(jti):
        JWTConfig.blacklisted_tokens.add(jti)