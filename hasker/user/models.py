from django.db import models

class User(models.Model):
    email=models.EmailField()
    login=models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    avatar = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    reg_date = models.DateTimeField(auto_now_add=True)