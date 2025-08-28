# themes/forms.py
from django import forms
from .models import Theme

class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = [
            "name", "description", "tags",
            "image", "is_draft", "priority"
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "tags": forms.TextInput(attrs={"class": "form-control"}),
            "priority": forms.NumberInput(attrs={"class": "form-control"}),
        }
