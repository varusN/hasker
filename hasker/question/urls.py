from django.urls import path

from . import views

app_name = "question"

urlpatterns = [
    path("", views.Questions.as_view(), name="index"),
    path("latest/", views.LatestQuestions.as_view(), name="latest"),
    path("top/", views.TopQuestions.as_view(), name="top"),
    path("search/", views.SearchQuestions.as_view(), name="search"),
    path("tag/<tag>", views.TagQuestions.as_view(), name="tag"),
    path("details/<int:question_id>/", views.details, name="details"),
    path("edit/<int:question_id>/", views.EditQuestion.as_view(), name="edit"),
    path("ask/", views.AskQuestion.as_view(), name="ask"),
    path("answer/<int:question_id>/", views.AnswerQuestion.as_view(), name="answer"),
    path("logout/", views.Questions.as_view(), name="logout"),
    path("signup/", views.TopQuestions.as_view(), name="signup"),
]
