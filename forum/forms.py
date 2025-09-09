from django import forms
from .models import Post, Thread, Category
from django.forms import ModelForm, TextInput, Textarea, DateTimeInput, DateInput


class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = ["content_text", "files"]
        widgets = {
            'content_text': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'пост',
                }),
                
                'files': forms.FileInput()
                }
        

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['category', 'theme', 'author','description', 'is_closed', 'image']
                
