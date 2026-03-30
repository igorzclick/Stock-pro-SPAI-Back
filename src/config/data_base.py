from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()
db = SQLAlchemy()

def init_db(app):
    DB_USER = os.getenv('POSTGRES_USER', 'root')
    DB_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'root')
    DB_HOST = os.getenv('POSTGRES_HOST', 'db')
    DB_PORT = os.getenv('POSTGRES_PORT', '5432')
    DB_NAME = os.getenv('POSTGRES_DB', 'marketManagement')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    with app.app_context():
        db.create_all()
        