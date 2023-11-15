from django.contrib.auth.models import User, AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    def formatted_joined_time(self):
        print(self.date_joined)
        return self.date_joined.strftime("%Y-%m-%d %H:%M") or "no joined time"