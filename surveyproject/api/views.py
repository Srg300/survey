from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Question, Survey, Answer, UserAnswer
from .serializer import *

from datetime import datetime, date

from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework import permissions

# Create your views here.

# /api/surveys/
@api_view(['GET'])
@permission_classes([AllowAny])
def get_survey_list(request):
    """ Получить список всех опросов """
    if request.user.is_staff:
        surveys = Survey.objects.all()
    else:
        surveys = Survey.objects.filter(is_active=True)
    serializer_survey = SurveyListSerializer(surveys, many=True)
    return Response(serializer_survey.data, status=status.HTTP_200_OK)


# /api/survey/create/  
@api_view(['POST'])
@permission_classes([AllowAny])
def create_survey(request):
    """ Создать опрос """
    if request.method == 'POST':
        recived_data = request.data
        serializer_survey = SurveyDetailSerializer(data=recived_data)
        if serializer_survey.is_valid():
            surveys = serializer_survey.save()
            return Response(serializer_survey.data, status=status.HTTP_200_OK)
        return Response(serializer_survey.errors, status=status.HTTP_400_BAD_REQUEST)


# /api/survey/{surv_id}
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def get_update_or_delete_survey(request, surv_id):
    """ Получить, обновить или удалить опрос по id """
    try:
        survey = Survey.objects.get(id=str(surv_id))
    except Survey.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer_survey = SurveyDetailSerializer(survey)
        return Response(serializer_survey.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        received_data = request.data
        serializer_survey = SurveyUpdateSerializer(survey, data=received_data)
        if serializer_survey.is_valid():
            surveys = serializer_survey.save()
            return Response(serializer_survey.data, status=status.HTTP_202_ACCEPTED)
        return Response(status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        survey.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# /api/questions/
@api_view(['GET'])
@permission_classes([AllowAny])
def get_questions_list(request):
    """ Получить список вопросов """
    questions = Question.objects.all()
    serializer_question = QuestionSerializer(questions, many=True)
    return Response(
        {'questions':serializer_question.data},
        status=status.HTTP_200_OK)

# /api/question/create/
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def get_or_create_question(request):
    """ Создать или получить список вопросов """
    if request.method == 'GET':
        questions = Question.objects.all()
        serializer_question = QuestionSerializer(questions, many=True)
        return Response(
            {'questions':serializer_question.data},
            status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        received_data = request.data
        serializer_question = QuestionSerializer(data=received_data)
        if serializer_question.is_valid():
            questions = serializer_question.save()
            return Response(serializer_question.data, status=status.HTTP_201_CREATED)   
        return Response(serializer_question.errors, status=status.HTTP_400_BAD_REQUEST)  


# /api/question/{question_id}
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def get_update_or_delete_question(request, question_id):
    """ Получить, обновить и удалить вопрос по id  """
    try:
        question = Question.objects.get(id=str(question_id))
    except Question.DoesNotExist:
        return Response(status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer_question = QuestionSerializer(question)
        return Response(serializer_question.data, status=status.HTTP_200_OK)

    if request.method == 'PUT':
        received_data = request.data
        serializer_question = QuestionSerializer(question, data=received_data)
        if serializer_question.is_valid():
            question = serializer_question.save()
            return Response(serializer_question.data, status=status.HTTP_202_ACCEPTED)
        return Response(status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([AllowAny])
def choose_surveу(request, survey_id):
    """Создать UserAnswer в системе, вернуть в Response user_uuid и использовать его в последующих запросах"""
    try:
        survey = Survey.objects.get(id=survey_id)
    except Survey.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    user_answer = UserAnswer()
    user_answer.survey = survey
    # сохраняем опрос в ответах юзера
    user_answer.save()

    # Теперь нужно вернуть 1 вопрос
    serializer_user_answer = UserAnswerSerializer(user_answer)
    question_id = user_answer.check_available_questions()

    if question_id is not None:
        question = Question.objects.get(id=question_id)
        serializer_quiestion = QuestionSerializer(question)
    else:
        return Response({'finished': 'Test is finished'}, status=status.HTTP_200_OK)
    return Response({'user_answer': serializer_user_answer.data, 'question': serializer_quiestion.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_answers_list(request):
    """ Получить список ответ """
    answers = Answer.objects.all()
    serializer_answer = AnswerSerializer(answers, many=True)
    return Response({'answer':serializer_answer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def answer(request, user_uuid):
    try:
        user_answer = UserAnswer.objects.get(user_uuid=user_uuid)
    except UserAnswer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # import pdb; pdb.set_trace()
    recieved_data = request.data
    question = Question.objects.get(id=recieved_data.get('question'))
    
    serializer_answer = AnswerSerializer(data=recieved_data)
    if serializer_answer.is_valid():
        ans = serializer_answer.save()
        user_answer.answers.add(ans)
        user_answer.save()
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    # Вернуть следующий вопрос
    serializer_user_answer = UserAnswerSerializer(user_answer)
    question_id = user_answer.check_available_questions()

    if question_id is not None:
        question = Question.objects.get(id=question_id)
        serializer_quiestion = QuestionSerializer(question)
    else:
        return Response({'finished': 'Test is finished'}, status=status.HTTP_200_OK)
    return Response({'user_answer': serializer_user_answer.data, 'question': serializer_quiestion.data}, status=status.HTTP_200_OK)    


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_answers_list(request):
    """ Получить список ответов пользователя на опрос """
    user_answers = UserAnswer.objects.all()
    serializer_user_answers = UserAnswerSerializer(user_answers, many=True)
    return Response({'user answers':serializer_user_answers.data}, status=status.HTTP_200_OK)



# class QuestionList(generics.ListAPIView):
#     serializer_class = QuestionSerializer
#     queryset = Question.objects.all()
#     permission_classes = [permissions.IsAdminUser]


# class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = QuestionSerializer
#     queryset = Question.objects.all()
#     permission_classes = [permissions.IsAdminUser]


# class QuestionCreate(generics.CreateAPIView):
#     serializer_class = QuestionSerializer
#     queryset = Question.objects.all()
#     permission_classes = [permissions.IsAdminUser]


# class AnswerCreate(generics.CreateAPIView):
#     serializer_class = AnswerSerializer
#     queryset = Answer.objects.all()


# class AnswerList(generics.ListAPIView):
#     serializer_class = AnswerSerializer
#     queryset = Answer.objects.all()

#     def get_queryset(self):
#         if self.request.user.is_staff:
#             answer = Answer.objects.all()
#             return answer
#         else:
#             user = self.request.user
#             answer = Answer.objects.filter(user=user)
#             return answer


# class AnswerDetail(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = AnswerSerializer
#     queryset = Answer.objects.all() 


# @api_view(['GET', 'POST'])
# def add_answer(request):
#     if request.method == 'GET':
#         answers = Answer.objects.all()
#         serializers_answer = AnswerSerializer(answers, many=True)
#         return Response({'result':serializers_answer.data}, status=status.HTTP_200_OK)
#     return Response(serializers_answer.errors, status=status.HTTP_400_BAD_REQUEST)    

#     if request.method == 'POST':
#         if request.user:
#             user_id = request.user.id
#             surv_id = Survey.objects.get(id=id)
#             question = Question.objects.get(id=id)
#             serializers_answer = AnswerSerializer(user_id, surv_id)
#             return Response({'result':serializers_answer.data}, status=status.HTTP_200_OK)
#     return Response(serializers_answer.errors, status=status.HTTP_400_BAD_REQUEST)    


# class SurveyList(generics.ListAPIView):
#     serializer_class = SurveyListSerializer
#     queryset = Survey.objects.all()

#     def get_queryset(self):
#         if self.request.user.is_staff:
#             surveys = Survey.objects.all()
#             return surveys
#         else:
#             surveys = Survey.objects.filter(is_active=True)
#             return surveys


# class SurveyDetail(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = SurveyDetailSerializer
#     queryset = Survey.objects.all()

#     def get_queryset(self):
#         if self.request.user.is_staff:
#             surveys = Survey.objects.all()
#             return surveys
#         else:
#             surveys = Survey.objects.filter(is_active=True)
#             return surveys


# class SurveyCreate(generics.CreateAPIView):
#     serializer_class = SurveyDetailSerializer
#     queryset = Survey.objects.all()
#     permission_classes = [permissions.IsAdminUser]


    