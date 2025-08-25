from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class Voting(models.Model):
    name = models.CharField(max_length=100)
    data_start = models.DateField(blank=True, null=True)
    data_end = models.DateField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors_voting')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Name" -{self.name}, author-{self.author}'

class Option(models.Model):
    name = models.CharField(max_length=100)
    voting = models.ForeignKey(Voting, on_delete=CASCADE, related_name='options')

    def __str__(self):
        return f'Name" -{self.name},'

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_votes')
    option_vote = models.ForeignKey(Option, on_delete=CASCADE, related_name='option_votes')
    voting = models.ForeignKey(Voting, on_delete=CASCADE, related_name='voting_votes')
    created_at = models.DateTimeField(auto_now_add=True)