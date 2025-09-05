from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView

from voting_system.mixins import UserIsOwnerMixins
from voting_system.models import Voting


class VoteListView(LoginRequiredMixin, ListView):
    model = Voting
    context_object_name = 'votes'
    template_name = 'voting_list.html'


class VoteDetailView(LoginRequiredMixin, DetailView):
    model = Voting
    context_object_name = 'vote'
    template_name = 'voting_detail.html'


class VoteCreateViwe(LoginRequiredMixin, CreateView):
    pass



class VoteDeleteView(LoginRequiredMixin, UserIsOwnerMixins, DeleteView):
    pass