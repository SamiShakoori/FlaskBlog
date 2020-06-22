from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, VARCHAR, String
from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(32), nullable=False, unique=False)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(120), nullable=False, unique=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
