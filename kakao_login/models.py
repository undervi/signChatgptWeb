from django.db import models

# Create your models here.
class Users(models.Model):
    user_id = models.CharField(primary_key=True, max_length=100)
    user_name = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=6,  null=True, blank=True)
    profile_imeage_url = models.CharField(max_length=100, null=True, blank=True)
    