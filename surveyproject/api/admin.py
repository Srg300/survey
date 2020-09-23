from django.contrib import admin
from api.models import Question, Survey, Answer, UserAnswer

# Register your models here.

admin.site.register(Question)
admin.site.register(Survey)
admin.site.register(Answer)
admin.site.register(UserAnswer)