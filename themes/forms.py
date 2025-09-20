# themes/forms.py
from django import forms
from .models import Theme

class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ["name", "background_color",  "background_image", "font_family", "custom_css"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "background_color": forms.TextInput(attrs={"type": "color", "class": "form-control form-control-color"}),
            
            "background_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "font_family": forms.Select(
                choices=[
                    ("Arial", "Arial"),
                    ("Helvetica", "Helvetica"),
                    ("Times New Roman", "Times New Roman"),
                    ("Georgia", "Georgia"),
                    ("Courier New", "Courier New"),
                    ("Verdana", "Verdana"),
                    ("Tahoma", "Tahoma"),
                    ("Roboto", "Roboto"),
                    ("Open Sans", "Open Sans"),
                    ("Lato", "Lato"),
                    ("Montserrat", "Montserrat"),
                    ("Monospace", "Monospace"),
                ],
                attrs={"class": "form-select"}
            ),
            "custom_css": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }