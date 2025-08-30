from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from voting_system.models import Voting


class VoteListView(LoginRequiredMixin, ListView):
    model = Voting
    template_name = 'voting_list.html'
