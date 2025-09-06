from django import forms
from .models import Post
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
                
