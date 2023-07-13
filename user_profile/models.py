from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_profile_pic = models.FileField(null=True, upload_to='static/avatars/')
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)