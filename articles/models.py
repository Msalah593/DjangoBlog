from django.db import models
from users.models import CustomUser
from django.conf import settings
# Create your models here.

class Article (models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,blank=False)
    body = models.CharField(max_length=200,blank=False)
    pub_date = models.DateTimeField('date published',auto_now_add=True)


    