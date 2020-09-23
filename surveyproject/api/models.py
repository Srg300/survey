from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    QUESTION_TYPES = [
    ('string type', 'ответ текстом'),
    ('pick one', 'ответ с выбором одного варианта'),
    ('pick many', 'ответ с выбором нескольких вариантов'),
    ]
    title = models.CharField(max_length=500, default='', blank=True)
    type_question = models.CharField(max_length=100,choices=QUESTION_TYPES, default=[0][0]) 
    
    def __str__(self):
        return self.title
    

class Survey(models.Model):
    title = models.CharField(max_length=500, default='', blank=True)
    discription = models.CharField(max_length=500, default='', blank=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True, blank=True)
    end_date = models.DateTimeField(auto_now=True, blank=True)
    questions = models.ManyToManyField(Question, blank=True)
    
    def __str__(self):
        return self.title


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, related_name='question_in_answer', on_delete=models.CASCADE)
    answer = models.CharField(max_length=500, default='', blank=True)
  
    # def __str__(self):
    #     return self.user_id + self.surv_id + self.question  
