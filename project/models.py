from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from datetime import timedelta
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
        if self.formatted_datetime_updated is None:
            return "Posted at " + self.formatted_datetime_created
        else:
            return f"Posted at {self.formatted_datetime_created()} (Last updated at {self.formatted_datetime_updated()})"

    def get_created_user_info(self):
        try:
            user = CustomUser.objects.get(id=self.user_created_id)
            return user
        except CustomUser.DoesNotExist:
            return None
    
    def get_completed_user_info(self):
        try:
            user = CustomUser.objects.get(id=self.user_completed_id)
            return user
        except CustomUser.DoesNotExist:
            return None
        
    def get_user_info(self, user_id: int):
        try:
            user = CustomUser.objects.get(id=user_id)
            return user
        except CustomUser.DoesNotExist:
            return None

    def get_time_ago(self) -> str:
        current_time = timezone.now()
        time_difference = current_time - self.datetime_created

        if time_difference < timedelta(minutes=1):
            # 1분 이내
            return '1 min ago'
        elif time_difference < timedelta(hours=1):
            # 1시간 이내
            minutes = int(time_difference.seconds / 60)
            return f'{minutes} mins ago'
        elif time_difference < timedelta(days=1):
            # 24시간 이내
            hours = int(time_difference.seconds / 3600)
            if hours == 1:
                return '1 hour ago'
            else:
                return f'{hours} hours ago'
        else:
            # 24시간 이상
            days = time_difference.days
            if days == 1:
                return '1 day ago'
            else:
                return f'{days} days ago'


    def formatted_datetime_created(self) -> str:
        return self.datetime_created.strftime("%Y-%m-%d %H:%M")


    def formatted_datetime_updated(self) -> str:
        return self.datetime_created.strftime("%Y-%m-%d %H:%M") or None

    def formatted_datetime_due(self) -> str:
        if self.date_due:
            return self.date_due.strftime("%Y-%m-%d")
        else:
            return "No due date"
        
class ProjectMemeber(models.Model):
    
    id = models.AutoField(primary_key=True)
        
    project_id = models.IntegerField()
    user_id = models.IntegerField()
    is_manager = models.BooleanField(default=False)
    
    class Meta:
        db_table = "project_member"