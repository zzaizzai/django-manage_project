from django.db import models
from typing import List

from manage_project.settings.database import Base, session
from sqlalchemy import Column, Integer, String, create_engine, DateTime, Date, Sequence, Boolean, Text, func


# # Create your models here.
# class MasterDepartment(models.Model):
    
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)
#     datetime_created = models.DateTimeField(auto_now_add=True)
#     datetime_updated = models.DateTimeField(auto_now=True, null=True)
    
#     class Meta:
#         db_table = "master_department"
        
    
#     def __str__(self):
#         return self.name
    

class MasterBaseModel(Base):
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    datetime_created = Column(DateTime(timezone=True), server_default=func.now())
    datetime_updated = Column(DateTime(timezone=True), server_default=func.now())
    
class MasterDepartment(MasterBaseModel):
    
    __tablename__ = 'master_department'
        
    def __str__(self):
        return self.name
    
    @classmethod
    def get_all_master_department(cls) -> List['MasterDepartment']:
        departments = session.query(MasterDepartment).order_by(MasterDepartment.id).all()
        return departments
        