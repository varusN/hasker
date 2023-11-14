import functools

from django.test import TestCase
from django.urls import resolve, reverse


def cases(cases):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args):
            for c in cases:
                new_args = args + (c if isinstance(c, tuple) else (c,))
                f(*new_args)

        return wrapper

    return decorator


class UrlTest(TestCase):
    @cases(
        [
            ("/ask/"),
            ("/user/logout/"),
            ("/user/password/"),
        ]
    )
    def test_redirect_url(self, arguments):
        print("test_url: ", arguments)
        response = self.client.get(arguments)
        self.assertEqual(response.status_code, 302)

    def test_wrong_url(self):
        url = "/dsntxst/"
        print("test_url: ", url)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_view_index_correct_template(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "question/question_list.html")

    def test_view_login_correct_template(self):
        response = self.client.get("/user/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/login.html")

    def test_view_signup_correct_template(self):
        response = self.client.get("/user/signup/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/register.html")

    def test_view_top_correct_template(self):
        response = self.client.get("/top/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "question/question_list.html")

    def test_view_latest_correct_template(self):
        response = self.client.get("/latest/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "question/question_list.html")
