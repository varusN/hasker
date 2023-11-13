from django.test import TestCase, Client
from question.models import Question
from apps.users.models import User
from django.core.urlresolvers import reverse


class QuestionListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User(username='user1', password='user_pass')
        user.save()
        for i in range(20):
            question = Question(
                title='title{0}'.format(i),
                content='content{0}'.format(i),
                create_by=user,
                vote_count=20-i
            )
            question.save()

    def setUp(self):
        self.client = Client()

    def test_list(self):
        response = self.client.get(reverse('qa:list'))
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.context[-1]['object_list'].count(), 20)

    def test_context_data(self):
        response = self.client.get(reverse('qa:list'), {'order_by': 'hot'})
        self.assertTrue(response.context[-1]['hot'])
        response = self.client.get(reverse('qa:list'))
        self.assertFalse(response.context[-1].get('hot', False))

    def test_queryset(self):
        response = self.client.get(reverse('qa:list'))
        self.assertEquals(response.context[-1]['object_list'].first().title, 'title19')
        self.assertEquals(response.context[-1]['object_list'].last().title, 'title0')

    def test_queryset_hot(self):
        response = self.client.get(reverse('qa:list'), {'order_by': 'hot'})
        self.assertEquals(response.context[-1]['object_list'].first().title, 'title0')
        self.assertEquals(response.context[-1]['object_list'].last().title, 'title19')


class QuestionSearchListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User(username='user1', password='user_pass')
        user.save()
        for i in range(20):
            question = Question(
                title='title{0}'.format(i),
                content='content{0}'.format(i),
                create_by=user,
                vote_count=20-i
            )
            question.save()

    def setUp(self):
        self.client = Client()

    def test_list(self):
        response = self.client.get(reverse('qa:search'))
        self.assertEqual(response.status_code, 200)

    def test_context_data(self):
        response = self.client.get(reverse('qa:search'), {'q': 'title'})
        self.assertEquals(response.context[-1]['current_q'], 'title')

    def test_queryset_title_search(self):
        response = self.client.get(reverse('qa:search'), {'q': 'title1'})
        self.assertEquals(response.context[-1]['object_list'].count(), 11)
        response = self.client.get(reverse('qa:search'), {'q': 'title10'})
        self.assertEquals(response.context[-1]['object_list'].count(), 1)
        response = self.client.get(reverse('qa:search'), {'q': 'title'})
        self.assertEquals(response.context[-1]['object_list'].count(), 20)

    def test_queryset_content_search(self):
        response = self.client.get(reverse('qa:search'), {'q': 'content19'})
        self.assertEquals(response.context[-1]['object_list'].count(), 1)
        response = self.client.get(reverse('qa:search'), {'q': 'content'})
        self.assertEquals(response.context[-1]['object_list'].count(), 20)

    def test_queryset_title_and_content_search(self):
        response = self.client.get(reverse('qa:search'), {'q': '19'})
        self.assertEquals(response.context[-1]['object_list'].count(), 1)


class QuestionTagListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User(username='user1', password='user_pass')
        user.save()
        tags = [
            'python,django',
            'python',
            'js,react',
            'drf',
        ]
        for i in range(20):
            question = Question(
                title='title{0}'.format(i),
                content='content{0}'.format(i),
                create_by=user,
                vote_count=20-i
            )
            question.save()
            question.save_tags(tags[i//5])

    def setUp(self):
        self.client = Client()

    def test_list(self):
        response = self.client.get(reverse('qa:tag', kwargs={'tag': 'python'}))
        self.assertEqual(response.status_code, 200)

    def test_context_data(self):
        response = self.client.get(reverse('qa:tag', kwargs={'tag': 'python'}))
        self.assertEquals(response.context[-1]['current_tag'], 'tag:python')

    def test_queryset(self):
        response = self.client.get(reverse('qa:tag', kwargs={'tag': 'python'}))
        self.assertEquals(response.context[-1]['object_list'].count(), 10)
        response = self.client.get(reverse('qa:tag', kwargs={'tag': 'django'}))
        self.assertEquals(response.context[-1]['object_list'].count(), 5)
        response = self.client.get(reverse('qa:tag', kwargs={'tag': 'js'}))
        self.assertEquals(response.context[-1]['object_list'].count(), 5)


class QuestionCreateViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User(username='user1', password='user_pass')
        user.save()
        tags = [
            'python,django',
            'python',
            'js,react',
            'drf',
        ]
        for i in range(20):
            question = Question(
                title='title{0}'.format(i),
                content='content{0}'.format(i),
                create_by=user,
                vote_count=20-i
            )
            question.save()
            question.save_tags(tags[i//5])

    def setUp(self):
        self.client = Client()

    def test_list(self):
        response = self.client.get(reverse('qa:create'))
        self.assertEqual(response.status_code, 200)

    def test_context_data(self):
        response = self.client.get(reverse('qa:create'))
        self.assertEquals(response.context[-1]['tags'].count(), 5)

    def add_answer(self):
        self.client.login(username='user1', password='user_pass')
        response = self.client.post(reverse('qa:create'), {
            'title': 'new_title',
            'content': 'new_content',
            'tags': 'python, flask',
        })
        self.assertEqual(response.status_code, 200)


