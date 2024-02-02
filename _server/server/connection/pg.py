from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from server.connection import db


 
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(50), unique=True, nullable=False)
    first_name = db.Column(String(50))
    last_name = db.Column(String(50))
    posts = relationship('Post', back_populates='user')

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(Integer, primary_key=True)
    text = db.Column(String, nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    user_id = db.Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='posts')
