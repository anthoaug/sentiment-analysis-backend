from django.contrib.auth.models import User
from django.db import models


class FollowedUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="followed_users", primary_key=True)
    followed = models.JSONField(default=dict)
