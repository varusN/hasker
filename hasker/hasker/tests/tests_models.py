from django.test import TestCase
from question.models import Answer, Question, Tag
from user.models import User, user_photo_path


class QuestionTest(TestCase):
    def setUp(self):
        user = User(
            username="testuser", email="test@usertest.com", password="testuserpass"
        )
        user.save()

    def test_create_question(self):
        user = User.objects.get(username="testuser")
        q = Question.objects.create(
            subject="subject", description="content", author=user
        )
        self.assertEquals(q.subject, "subject")
        self.assertEquals(q.description, "content")
        self.assertEquals(q.author.username, user.username)

    def test_create_question_w_tags(self):
        user = User.objects.get(username="testuser")
        q = Question.objects.create(
            subject="subject", description="content", author=user
        )
        q.add_tags({"tag1", "tag2", "tag3"})
        self.assertEquals(q.subject, "subject")
        self.assertEquals(q.description, "content")
        self.assertEquals(q.author.username, user.username)
        self.assertEquals(q.tag.get(name="tag1").name, "tag1")
        self.assertEquals(q.tag.get(name="tag2").name, "tag2")
        self.assertEquals(q.tag.get(name="tag3").name, "tag3")
