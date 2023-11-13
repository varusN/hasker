from typing import List

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from user.models import User


class Question(models.Model):
    subject = models.CharField(max_length=255)
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
    def trending(cls, count: int = 5) -> models.QuerySet:
        return cls.objects.order_by("-votes")[:count]

    @classmethod
    def get_question(cls, pk):
        if pk:
            obj = get_object_or_404(cls, pk=pk)
            return obj
        else:
            raise Http404

    @classmethod
    def add_tags(self, tags: List[str], user):
        if self.pk is None:
            raise ValueError("Instance should be saved.")
        for raw_tag in tags:
            try:
                tag = Tag.objects.get(name=raw_tag)
            except ObjectDoesNotExist:
                tag = Tag.objects.create(added=user, name=raw_tag)
            self.tag.add(tag)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField()
    is_correct = models.BooleanField(default=0, blank=True)
    votes = models.IntegerField(default=0, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_answers(question_id):
        return Answer.objects.filter(question__id=question_id).order_by(
            "-votes", "-created_date"
        )


class Tag(models.Model):
    added = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="added_tags",
        related_query_name="added_tag",
    )
    name = models.CharField(blank=False, max_length=settings.QUESTIONS_TAGS_LENGTH)

    def __str__(self):
        return self.name
