from django.db import models
from kakao_login.models import Users


class Board(models.Model):
    board_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False) 