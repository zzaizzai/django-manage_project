from datetime import timedelta, datetime
from typing import Union, Any, List, Optional

from django.db import models
from accounts.models import CustomUser
from django.utils import timezone

# Create your models here.


class PostBaseModel(models.Model):
    
    id = models.AutoField(primary_key=True)
    user_created_id = models.IntegerField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract  = True
        
        
    def get_user_info_with_id(self, user_id: int) -> Optional[CustomUser]:
        try:
            user = CustomUser.objects.get(id=user_id)
            return user
        except:
            return None
        
    def get_created_user_info(self) -> Optional[CustomUser]:
        return self.get_user_info_with_id(self.user_created_id)
        
    def show_time_created_with_updated(self) -> str:
        if self.formatted_datetime_updated() is None:
            return "Posted at " + self.formatted_datetime_created()
        return f"Posted at {self.formatted_datetime_created()} (Last updated at {self.formatted_datetime_updated()})"
    
    def formatted_datetime_created(self) -> str:
        return self.datetime_created.strftime("%Y-%m-%d %H:%M") or "Time Error"

    def formatted_datetime_updated(self) -> Union[str, None]:
        if self.datetime_created == self.datetime_updated or self.datetime_updated is None:
            return None
        return self.datetime_created.strftime("%Y-%m-%d %H:%M") or None

    def show_time_created_ago(self):
        return self.formatted_time_ago(self.datetime_created)
    
    def formatted_time_ago(self, datetime: datetime) -> str:
        current_time = timezone.now()
        time_difference = current_time - datetime
        
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
            
            
class Project(PostBaseModel):
    
    title = models.CharField(max_length=100)
    
    user_completed_id = models.IntegerField(null=True)
    text = models.TextField()
    
    datetime_completed = models.DateTimeField(null=True)
    date_due = models.DateField(null=True)
    datetime_cancled = models.DateTimeField(null=True)
    
    is_cancled = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    class Meta:
        db_table = "projects"

    def __str__(self):
        return self.title
    
    def get_completed_user_info(self) -> Optional[CustomUser]:
        self.get_user_info_with_id(self.user_completed_id)
        
    def get_comments(self) -> List['ProjectComment']:
        comments = ProjectComment.objects.filter(project_id=self.id).order_by('datetime_created')
        return list(comments)
            
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
    
    def get_status_str(self) -> str:
        if self.is_cancled is True:
            return "Cancled"
        if self.is_completed is True:
            return "Completed"
        return "Proceeding"


class ProjectComment(PostBaseModel):
    
    project_id = models.IntegerField()
    text = models.TextField()
    
    class Meta:
        db_table = "project_comment"
    
    
    @classmethod
    def create_comment(cls, user_id: int, project_id: int, text: str) -> 'ProjectComment':
        comment = cls(user_created_id=user_id, project_id=project_id, text=text)
        comment.save()
        return comment


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
