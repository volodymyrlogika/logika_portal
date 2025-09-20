from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import DateInput
from .models import  Portfolio


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['user', 'title', 'description', 'link', 'created_at']

        widgets = {
             'created_at': forms.DateTimeInput(attrs={
                 'type': 'datetime-local',
                 'class': 'form-control',
             }),
         }
        
        