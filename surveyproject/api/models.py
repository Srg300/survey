from django.db import models
from django.contrib.auth.models import User

import uuid

class Question(models.Model):
    QUESTION_TYPES = [
    ('string type', 'ответ текстом'),
    ('pick one', 'ответ с выбором одного варианта'),
    ('pick many', 'ответ с выбором нескольких вариантов'),
    ]
    title = models.CharField(max_length=500, default='', blank=True)
    type_question = models.CharField(max_length=100,choices=QUESTION_TYPES, default='string type') 
    
    def __str__(self):
        return self.title
    

class Survey(models.Model):
    title = models.CharField(max_length=500, default='', blank=True)
    discription = models.CharField(max_length=500, default='', blank=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True, blank=True)
    end_date = models.DateTimeField(auto_now=True, blank=True)
    questions = models.ManyToManyField(Question, blank=True)

    def sorted_questions(self):
        return sorted([q.id for q in self.questions.all()])
    
    def __str__(self):
        return self.title


class Answer(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # survey = models.ForeignKey(Survey, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=500, default='', blank=True)


class UserAnswer(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user_uuid = models.CharField(max_length=100, default=uuid.uuid1, blank=True)
    answers =  models.ManyToManyField(Answer, blank=True)
    is_finished = models.BooleanField(default=False)

    def check_available_questions(self):
        questions_left = list(set(self.survey.sorted_questions()).difference(set([a.question.id for a in self.answers.all()])))
        if questions_left:
            return questions_left[0]
        else:
            self.is_finished = True
            self.save()
            return None
