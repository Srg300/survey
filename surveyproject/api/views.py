from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Question, Survey, Answer
from .serializer import *

from datetime import datetime, date

from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import permissions

# Create your views here.



class SurveyList(generics.ListAPIView):
    serializer_class = SurveyListSerializer
    queryset = Survey.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff:
            surveys = Survey.objects.all()
            return surveys
        else:
            surveys = Survey.objects.filter(is_active=True)
            return surveys
    


class SurveyDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SurveyDetailSerializer
    queryset = Survey.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff:
            surveys = Survey.objects.all()
            return surveys
        else:
            surveys = Survey.objects.filter(is_active=True)
            return surveys


class SurveyCreate(generics.CreateAPIView):
    serializer_class = SurveyDetailSerializer
    queryset = Survey.objects.all()
    permission_classes = [permissions.IsAdminUser]


class QuestionList(generics.ListAPIView):
    serializer_class = QuestionListSerializer
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAdminUser]


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionListSerializer
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAdminUser]


class QuestionCreate(generics.CreateAPIView):
    serializer_class = QuestionListSerializer
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAdminUser]


class AnswerCreate(generics.CreateAPIView):
    serializer_class = AnswerCreateSerializer
    queryset = Answer.objects.all()


class AnswerList(generics.ListAPIView):
    serializer_class = AnswerDetailSerializer
    queryset = Answer.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff:
            answer = Answer.objects.all()
            return answer
        else:
            user = self.request.user
            answer = Answer.objects.filter(user=user)
            return answer


class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnswerDetailSerializer
    queryset = Answer.objects.all() 


@api_view(['GET', 'POST'])
def add_answer(request):
    if request.method == 'GET':
        answers = Answer.objects.all()
        serializers_answer = AnswerDetailSerializer(answers, many=True)
        return Response({'result':serializers_answer.data}, status=status.HTTP_200_OK)
    return Response(serializers_answer.errors, status=status.HTTP_400_BAD_REQUEST)    

    if request.method == 'POST':
        if request.user:
            user_id = request.user.id
            surv_id = Survey.objects.get(id=id)
            question = Question.objects.get(id=id)
            serializers_answer = AnswerDetailSerializer(user_id, surv_id)
            return Response({'result':serializers_answer.data}, status=status.HTTP_200_OK)
    return Response(serializers_answer.errors, status=status.HTTP_400_BAD_REQUEST)    




@api_view(['GET'])
def get_survey_list(request):
    if request.method == 'GET':
        surveys = Survey.objects.all()
        serializers_survey = SurveyListSerializer(surveys, many=True)
        return Response({'results': serializers_survey.data},status=status.HTTP_200_OK)
    return Response(serializers_survey.errors, status=status.HTTP_400_BAD_REQUEST)      