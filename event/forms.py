from django import forms
from .models import Event

class EventForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'speciality']
        widgets = {
            "date": forms.DateTimeInput(attrs={'type': 'date'})

        }

class EventFilterForm(forms.Form):
    speciality = (
        ("", 'Усі події'),
        ("низька", 'низька'),
        ('середня', "середня"),
        ('висока', "висока"),
        ('дуже висока', "дуже висока")
    )
    speciality = forms.ChoiceField(choices=speciality, required=False, label='Важливість події  ')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})