from django import forms
from .models import Post, Thread, Category, ReplyPost
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
        fields = ['category', 'theme','description', 'is_closed', 'image']
    widgets = {
        'image':forms.ImageField()
    }

class ReplyPostForm(forms.ModelForm):
    class Meta:
        model = ReplyPost
        fields = ["content_text", "files", "post"]