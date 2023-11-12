from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Project(models.Model):

    id = models.AutoField(primary_key=True)
    
    title = models.CharField(max_length=100)
    
    user_created = models.IntegerField()
    user_completed = models.IntegerField(null=True)
    text = models.TextField()
    
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_completed = models.DateTimeField(null=True)
    datetime_updated = models.DateTimeField(auto_now_add=True)
    date_due = models.DateField(null=True)
    datetime_cancled = models.DateTimeField(null=True)
    
    is_cancled = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    class Meta:
        db_table = "projects"

    def __str__(self):
        return self.title


class ProjectMemeber(models.Model):
    
    id = models.AutoField(primary_key=True)
        
    project_id = models.IntegerField()
    user_id = models.IntegerField()
    is_manager = models.BooleanField(default=False)
    
    class Meta:
        db_table = "project_member"