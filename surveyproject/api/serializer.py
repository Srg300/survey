from rest_framework import serializers, fields
from django.contrib.auth.models import User
from .models import Question, Answer, Survey, UserAnswer



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


class SurveyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['title', 'discription', 'is_active', 'end_date', 'questions' ]



class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'title', 'type_question']


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'




