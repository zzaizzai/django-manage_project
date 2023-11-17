from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from datetime import timedelta
from typing import Union, Any, List
# Create your models here.


class Project(models.Model):

    id = models.AutoField(primary_key=True)
    
    title = models.CharField(max_length=100)
    
    user_created_id = models.IntegerField()
    user_completed_id = models.IntegerField(null=True)
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
    
    
    def show_time_created_with_updated(self) -> str:
        if self.formatted_datetime_updated() is None:
            return "Posted at " + self.formatted_datetime_created()
        return f"Posted at {self.formatted_datetime_created()} (Last updated at {self.formatted_datetime_updated()})"

    def get_created_user_info(self) -> CustomUser:
        try:
            user = CustomUser.objects.get(id=self.user_created_id)
            return user
        except CustomUser.DoesNotExist:
            return None
    
    def get_completed_user_info(self) -> CustomUser:
        try:
            user = CustomUser.objects.get(id=self.user_completed_id)
            return user
        except CustomUser.DoesNotExist:
            return None
        
    def get_user_info(self, user_id: int) -> CustomUser:
        try:
            user = CustomUser.objects.get(id=user_id)
            return user
        except CustomUser.DoesNotExist:
            return None

    def get_time_ago(self) -> str:
        current_time = timezone.now()
        time_difference = current_time - self.datetime_created

        if time_difference < timedelta(minutes=1):
            # under 1min
            return '1 min ago'
        elif time_difference < timedelta(hours=1):
            # under 1hour
            minutes = int(time_difference.seconds / 60)
            return f'{minutes} mins ago'
        elif time_difference < timedelta(days=1):
            # under 24hours
            hours = int(time_difference.seconds / 3600)
            if hours == 1:
                return '1 hour ago'
            else:
                return f'{hours} hours ago'
        else:
            # over 24hours
            days = time_difference.days
            if days == 1:
                return '1 day ago'
            else:
                return f'{days} days ago'

    def formatted_datetime_created(self) -> str:
        return self.datetime_created.strftime("%Y-%m-%d %H:%M") or ""

    def formatted_datetime_updated(self) -> Union[str, None]:
        if self.datetime_created == self.datetime_updated:
            return None
        return self.datetime_created.strftime("%Y-%m-%d %H:%M") or None

    def formatted_datetime_due(self) -> str:
        if self.date_due:
            return self.date_due.strftime("%Y-%m-%d")
        return "No due date"
    
    def get_members(self) -> List['ProjectMemeber'] :
        members = ProjectMemeber.objects.filter(project_id = self.id)
        return list(members)
        
        
    def get_status_color(self) -> str:
        
        if self.is_cancled is True :
            return 'gray'
        
        if self.is_completed is True :
            return 'blue'
        
        return 'black'
        
class ProjectMemeber(models.Model):
    
    id = models.AutoField(primary_key=True)
    
    project_id = models.IntegerField()
    user_id = models.IntegerField()
    is_manager = models.BooleanField(default=False)
    
    class Meta:
        db_table = "project_member"
        
    def get_project_info(self) -> Project:
        return Project.objects.get(id=self.project_id)
        
    def get_user_info(self):
        return CustomUser.objects.get(id=self.user_id)
