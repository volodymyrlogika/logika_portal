from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class Voting(models.Model):
    name = models.CharField(max_length=100, verbose_name='Назва голосування')
    data_start = models.DateField(blank=True, null=True, verbose_name='Початок голосування')
    data_end = models.DateField(blank=True, null=True, verbose_name='Кінець голосування')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors_voting', verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Створено в ')
    
    def __str__(self):
        return f'Name" -{self.name}, author-{self.author}'
    
    class Meta:
        verbose_name = 'Голосування'
        verbose_name_plural = 'Голосування'
        ordering = ['-created_at']


class Option(models.Model):
    name = models.CharField(max_length=100, verbose_name='Варіант')
    voting = models.ForeignKey(Voting, on_delete=CASCADE, related_name='options', verbose_name='Голосування')

    def __str__(self):
        return f'Name" -{self.name},'
    
    class Meta:
        verbose_name = 'Варіанти голосування'
        verbose_name_plural = 'Варіанти голосування'
        ordering = ['name']

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_votes', verbose_name='Голосування людей')
    option_vote = models.ForeignKey(Option, on_delete=CASCADE, related_name='option_votes', verbose_name='Вибір голосування')
    voting = models.ForeignKey(Voting, on_delete=CASCADE, related_name='voting_votes', verbose_name='Збереження голосовань')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Зробленно в ')