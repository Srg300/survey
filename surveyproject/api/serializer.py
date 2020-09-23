from rest_framework import serializers, fields
from django.contrib.auth.models import User
from .models import Question, Answer, Survey



class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class SurveyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'title', 'discription', 'is_active', 'start_date', 'end_date', 'questions' ]
        depth = 1


class SurveyDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Survey
        fields = ['id', 'title', 'discription', 'is_active', 'start_date', 'end_date', 'questions' ]
        # ReadOnlyField = ['start_date']


class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['user_id', 'surv_id', 'question', 'answer']


class AnswerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['user', 'survey', 'question', 'answer']


class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['user', 'survey', 'question', 'answer']

