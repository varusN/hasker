from django.test import TestCase
from question.models import Question, Answer, Tag
from user.models import User

class QuestionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User(username='user1', password='user_pass')
        user.save()

    def test_create(self):
        user = User.objects.first()
        q = Question.objects.create(subject='subject', description='content', author=user)
        self.assertEquals(q.subject, 'subject')
        self.assertEquals(q.description, 'content')
        self.assertEquals(q.author.username, user.username)

    def test_save_tags(self):
        user = User.objects.first()
        q = Question.objects.create(subject='subject', description='content', author=user)
        q.add_tags({'python','django','mango'}, user)
        self.assertEquals(q.tags.count(), 3)
        self.assertEquals(q.tags.get(subject='python').title, 'python')
        self.assertEquals(q.tags.get(subject='django').title, 'django')
        self.assertEquals(q.tags.get(subject='mango').title, 'mango')

        q = Question.objects.create(subject='title2', description='content2', author=user)

        q.add_tags({'cython', 'django', 'mango', 'gango'}, user)
        self.assertEquals(q.tags.count(), 4)
        self.assertEquals(q.tags.get(subject='cython').subject, 'cython')
        self.assertEquals(q.tags.get(subject='django').subject, 'django')
        self.assertEquals(q.tags.get(subject='mango').subject, 'mango')
        self.assertEquals(q.tags.get(subject='gango').subject, 'gango')