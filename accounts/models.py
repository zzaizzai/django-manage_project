from django.contrib.auth.models import User, AbstractUser
from django.db import models
from maintenance.models import MasterDepartment

class CustomUser(AbstractUser):

    department_id = models.IntegerField(default=1)
    is_manager = models.BooleanField(default=False)
    
    def formatted_joined_time(self) -> str:
        return self.date_joined.strftime("%Y-%m-%d %H:%M") or "no joined time"
    
    def get_department_info(self):
        return MasterDepartment.objects.get(id=self.department_id) or "no department name"
    
    

