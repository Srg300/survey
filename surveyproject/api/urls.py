from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('surveys/', views.get_survey_list),
    path('survey/<int:surv_id>/', views.get_update_or_delete_survey),
    path('survey/create/', views.create_survey),

    path('questions/', views.get_questions_list),
    path('question/<int:question_id>/', views.get_update_or_delete_question),
    path('question/create/', views.get_or_create_question),

    path('survey/start/<int:survey_id>/', views.choose_surveу),
    
    # path('answer/add/', AnswerCreate.as_view()),
    path('answers/', views.get_answers_list),
    path('answer/add/<slug:user_uuid>/', views.answer),

    path('useranswers/', views.get_user_answers_list),


]