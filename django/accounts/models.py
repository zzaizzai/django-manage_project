from typing import List

from django.contrib.auth.models import User, AbstractUser
from django.db import models
from maintenance.models import MasterDepartment



#* Original Django Model
class CustomUser(AbstractUser):

    department_id = models.IntegerField(default=1)
    is_manager = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    