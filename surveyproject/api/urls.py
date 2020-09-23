from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('surveys/', SurveyList.as_view()),
    path('survey/<int:pk>/', SurveyDetail.as_view()),
    path('survey/create/', SurveyCreate.as_view()),

    path('questions/', QuestionList.as_view()),
    path('question/<int:pk>/', QuestionDetail.as_view()),
    path('question/create/', QuestionCreate.as_view()),

    path('answer/add/', AnswerCreate.as_view()),
    path('answers/', AnswerList.as_view()),
    path('answer/<int:pk>/', AnswerDetail.as_view()),


]