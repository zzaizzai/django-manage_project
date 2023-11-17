from django.db import models


# Create your models here.
class MasterDepartment(models.Model):
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = "master_department"
        
    
    def __str__(self):
        return self.name