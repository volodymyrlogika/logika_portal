from django import forms
from .models import Quiz, Question, AnswerOption


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['name', 'discription']  # поля, які видно у формі
        labels = {
            'name': "Назва опитування",
            'discription': "Опис"
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'text', 'page_number']
        labels = {
            'question': "Опитування",
            'text': "Текст питання",
            'page_number': "Номер сторінки"
        }


class AnswerOptionForm(forms.ModelForm):
    class Meta:
        model = AnswerOption
        fields = ['question', 'text']
        labels = {
            'question': "Питання",
            'text': "Варіант відповіді"
        }
