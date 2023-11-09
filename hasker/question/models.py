from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from user.models import User


VOTE_UP = 1
VOTE_DOWN = -1
VOTES = ((VOTE_UP, "Top Up"), (VOTE_DOWN, "Top Down"))

class Question(models.Model):
    subject = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=255)

    def publish(self):
        self.created_date = timezone.now()
        self.save()
    def __str__(self):
        return self.subject

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField()
    is_correct = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
