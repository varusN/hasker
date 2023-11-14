from typing import List

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from user.models import User


class Question(models.Model):
    subject = models.CharField(max_length=255, null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField("Tag", related_name="tags")
    votes = models.IntegerField(default=0, blank=True)
    answers = models.IntegerField(default=0, blank=True)

    def __str__(self):
        (self.subject,)
        (self.author,)
        (self.description,)
        (self.created_date,)
        (self.votes,)
        (self.answers,)
        (", ".join(t.name for t in self.tag.all()),)
        return self.subject

    @classmethod
    def trending(cls, count):
        return cls.objects.filter(votes__gt=0).order_by("-votes")[:count]

    @classmethod
    def get_question(cls, pk):
        if pk:
            obj = get_object_or_404(cls, pk=pk)
            return obj
        else:
            raise Http404

    def add_tags(self, tags):
        for t in tags:
            try:
                tag = Tag.objects.get(name=t)
            except ObjectDoesNotExist:
                tag = Tag.objects.create(name=t)
            self.tag.add(tag)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField()
    is_correct = models.BooleanField(default=0, blank=True)
    votes = models.IntegerField(default=0, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    name = models.CharField(blank=False, max_length=settings.QUESTIONS_TAGS_LENGTH)

    def __str__(self):
        return self.name
