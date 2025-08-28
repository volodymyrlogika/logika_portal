from django import forms
from .models import GalleryItem
from taggit.forms import TagField

class GalleryItemForm(forms.ModelForm):
    tags = TagField(required=False, help_text="Введіть теги через кому")  

    class Meta:
        model = GalleryItem
        fields = ["title", "file", "tags", "age_rating"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "age_rating": forms.Select(attrs={"class": "form-select"}),
        }
