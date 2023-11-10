from django.urls import path

from . import views

app_name = 'question'

urlpatterns = [
    path('', views.Questions.as_view(), name='index'),
    path('latest/', views.LatestQuestions.as_view(), name='latest'),
    path('top/', views.TopQuestions.as_view(), name='top'),
    path("search/", views.SearchQuestions.as_view(), name="search"),
    path("tag/<tag>", views.TagQuestions.as_view(), name="tag"),
    path('details/<int:question_id>/', views.Details.as_view(), name='details'),
    path('ask/', views.AskQuestion.as_view(), name='ask'),
    path('search/', views.Questions.as_view(), name='search'),
    path('profile/', views.Questions.as_view(), name='profile'),
    path('logout/', views.Questions.as_view(), name='logout'),
    path('login/', views.Questions.as_view(), name='login'),
    path('signup/', views.Questions.as_view(), name='signup'),

]
