from django.contrib import admin

from django.contrib import admin
from .models import Quiz, Question, AnswerOption, UserAnswer

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(AnswerOption)
admin.site.register(UserAnswer)

