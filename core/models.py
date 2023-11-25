from datetime import timedelta, datetime
from django.db import models
from manage_project.settings.database import Base, session

from typing import Optional
# Create your models here.
from sqlalchemy import Column, Integer, String, create_engine, DateTime, Date, Sequence, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from django.utils import timezone

class MyModel(Base):
    __tablename__ = 'my_model'
    id = Column(Integer, primary_key=True)
    
class CustomUser(Base):
    __tablename__ = 'accounts_customuser'
    
    id = Column(Integer, Sequence('accounts_customuser_id_seq'), primary_key=True)
    last_login = Column(DateTime)
    username  = Column(String(150))
    last_name = Column(String(150))
    first_name = Column(String(150))
    email = Column(String(254))
    password = Column(String(128))
    is_supseruser = Boolean()
    is_staff = Boolean()
    is_active = Boolean()
    is_manager = Boolean()

    def __str__(self):
        return self.username
class AAA(Base):
    __tablename__ = 'aaa'

    id = Column(Integer, primary_key=True)
    last_login = Column(DateTime)
    username = Column(String(150))
    password = Column(String(128))
    is_supseruser = Boolean()
    
class PostBaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_created_id =Column(Integer())
    datetime_created = Column(DateTime())
    datetime_updated = Column(DateTime())
    
    

    def show_time_created_ago(self):
        import pytz
        
        # print(type(self.datetime_created))
        # tt = self.datetime_created.replace(tzinfo=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        # print(type(tt))
        # print('created' , tt)
        # print(type(timezone.now()))
        # ss = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        # print('timezone'  ,timezone.now().strftime('%Y-%m-%d %H:%M:%S'))
        # time_difference = tt - ss
        # print(time_difference)
        # time_difference = self.datetime_created.replace(tzinfo=timezone.utc)  - self.datetime_created
        return ''
        # return self.formatted_time_ago(self.datetime_created)
    
    def formatted_time_ago(self, datetime_param: datetime) -> str:
        
        current_time = timezone.now()

        # datetime_param을 타임존이 설정된 datetime 객체로 변환합니다.
        datetime_param = timezone.make_aware(timezone.make_naive(datetime_param), timezone=timezone.utc)

        # 시간 차이를 계산합니다.
        time_difference = current_time - datetime_param
        
        if time_difference < timedelta(minutes=1):
            # under 1min
            seconds = int(time_difference.seconds)
            if seconds <= 10:
                return 'Now'
            return f'{seconds} sec'
        elif time_difference < timedelta(hours=1):
            # under 1hour
            minutes = int(time_difference.seconds / 60)
            if minutes == 1:
                return '1 min'
            return f'{minutes} mins'
        elif time_difference < timedelta(days=1):
            # under 24hours
            hours = int(time_difference.seconds / 3600)
            if hours == 1:
                return '1 hour'
            return f'{hours} hours'
        else:
            # over 24hours
            days = time_difference.days
            if days == 1:
                return '1 day'
            return f'{days} days'
            
            
    
    def get_created_user_info(self):
        user = session.query(CustomUser).filter_by(id=self.user_created_id).first()
        return user if user else None

class Project(PostBaseModel):
    
    __tablename__ = 'projects'
    
    title = Column(String(100))
    
    user_completed_id = Column(Integer, nullable=True)
    text = Column(Text)
    
    datetime_completed = Column(DateTime, nullable=True)
    date_due = Column(Date, nullable=True)
    datetime_canceled = Column(DateTime, nullable=True)
    
    is_canceled = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    
    def __str__(self):
        return self.title
    
    