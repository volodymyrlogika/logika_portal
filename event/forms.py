from django import forms
from .models import Event

class EventForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields():
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'speciality']