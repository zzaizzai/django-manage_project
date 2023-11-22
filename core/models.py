from django.db import models
from manage_project.settings.database import Base
# Create your models here.
from sqlalchemy import Column, Integer, String, create_engine, DateTime, Sequence, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class MyModel(Base):
    __tablename__ = 'my_model'
    id = Column(Integer, primary_key=True)
    
class CustomUser(Base):
    __tablename__ = 'accounts_customuser'
    
    id = Column(Integer, Sequence('account_user_id_seq'), primary_key=True)
    last_login = Column(DateTime)
    username = Column(String(150))
    password = Column(String(128))
    is_supseruser = Boolean()