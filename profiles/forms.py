from django import forms
from django.contrib.auth.models import User
from themes.models import Theme  # якщо у тебе є модель Theme

class ProfileForm(forms.ModelForm):
    theme = forms.ModelChoiceField(
        queryset=Theme.objects.all(),
        required=False,
        empty_label="(за замовчуванням)"
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
