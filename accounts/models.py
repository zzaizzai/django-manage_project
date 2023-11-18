from typing import List

from django.contrib.auth.models import User, AbstractUser
from django.db import models
from maintenance.models import MasterDepartment


class CustomUser(AbstractUser):

    department_id = models.IntegerField(default=1)
    is_manager = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
    @property
    def name(self) -> str:
        return self.username
    
    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    def formatted_joined_time(self) -> str:
        return self.date_joined.strftime("%Y-%m-%d %H:%M") or "no joined time"
    
    def get_department_info(self):
        return MasterDepartment.objects.get(id=self.department_id) or "no department name"
    
    def get_projects(self): # -> List['ProjectMemeber']
        from project.models import ProjectMemeber
        
        user_memeber_list = list(ProjectMemeber.objects.filter(user_id = self.id))
        projects = [user_member.get_project_info() for user_member in user_memeber_list]
            
        return  projects

    def get_number_projects_completed(self) -> int:
        projects = self.get_projects()
        
        count_completed = 0
        for project in projects:
            if project.is_completed is True and project.is_cancled is False:
                count_completed += 1
        
        return count_completed
    
    def get_number_projects_cancled(self) -> int:
        projects = self.get_projects()
        
        count_cancled = 0
        for project in projects:
            if project.is_cancled is True:
                count_cancled += 1
        
        return count_cancled
    
    def get_number_projects(self) -> int:
        return  len(self.get_projects())
    