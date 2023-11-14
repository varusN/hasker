from django.test import TestCase
from django.urls import resolve, reverse
from question.models import Answer, Question, Tag
from user.models import User


class QuestionView(TestCase):
    @classmethod
    def setUp(cls):
        user = User(
            username="testuser", email="test@usertest.com", password="testuserpass"
        )
        user.save()
        for i in range(11):
            question = Question(
                subject="Subject_{0}".format(i),
                description="description_{0}".format(i),
                author=user,
                votes=99 - 1,
            )
            question.save()
            question.add_tags({"tag1", "tag2", "otus"})

    def test_queryset_subject_search(self):
        response = self.client.get(reverse("question:search"), {"q": "Subject_2"})
        self.assertEquals(response.context[-1]["object_list"].count(), 1)
        response = self.client.get(reverse("question:search"), {"q": "Subject_1"})
        self.assertEquals(response.context[-1]["object_list"].count(), 2)
        response = self.client.get(reverse("question:search"), {"q": "Subject"})
        self.assertEquals(response.context[-1]["object_list"].count(), 11)

    def test_queryset_description_search(self):
        response = self.client.get(reverse("question:search"), {"q": "description_5"})
        self.assertEquals(response.context[-1]["object_list"].count(), 1)
        response = self.client.get(reverse("question:search"), {"q": "description_1"})
        self.assertEquals(response.context[-1]["object_list"].count(), 2)

    def test_queryset_title_and_content_search(self):
        response = self.client.get(reverse("question:search"), {"q": "2"})
        self.assertEquals(response.context[-1]["object_list"].count(), 1)
        response = self.client.get(reverse("question:search"), {"q": "1"})
        self.assertEquals(response.context[-1]["object_list"].count(), 2)

    def test_queryset_tag_search(self):
        response = self.client.get(reverse("question:tag", kwargs={"tag": "otus"}))
        self.assertEquals(response.context[-1]["object_list"].count(), 11)

    def test_queryset_top(self):
        response = self.client.get(reverse("question:top"))
        self.assertEquals(response.context[-1]["object_list"].count(), 11)

    def test_queryset_latest(self):
        response = self.client.get(reverse("question:latest"))
        self.assertEquals(response.context[-1]["object_list"].count(), 11)
