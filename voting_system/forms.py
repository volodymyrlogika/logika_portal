from django import forms


class CreateVotingForm(forms.Form):
    name = forms.CharField(label='Назва голосування', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    data_start = forms.DateTimeField(label='Початок голосування', widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))
    data_end = forms.DateTimeField(label='Кінець голосування', widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))
    option_1 = forms.CharField(label='Відповідь 1', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    option_2 = forms.CharField(label='Відповідь 2', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
