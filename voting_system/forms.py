from django import forms
from voting_system.models import *

class VotingForm(forms.ModelForm):
    class Meta:
        model = Voting
        fields = ['name', 'data_start', 'data_end']
        widgets = {
            'data_start': forms.DateInput(attrs={'type': 'date'}),
            'data_end': forms.DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super(VotingForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['data_start'].widget.attrs['class'] += ' my-custom=datepicker'

