from django import forms
from .models import GalleryItem

class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ["title", "file", "tags", "age_rating"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "age_rating": forms.Select(attrs={"class": "form-select"}),
        }
