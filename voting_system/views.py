from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, DeleteView

from voting_system.mixins import UserIsOwnerMixins
from voting_system.models import *


class VoteListView(LoginRequiredMixin, ListView):
    model = Voting
    context_object_name = 'votes'
    template_name = 'voting_list.html'


class VoteDetailView(LoginRequiredMixin, DetailView):
    model = Voting
    context_object_name = 'vote'
    template_name = 'voting_system/voting_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        voting = self.get_object()
        vote = Vote.objects.filter(voting=voting, user=self.request.user).first()
        if vote:
            context['user_voted'] = vote
        return context


    def post(self, request, *args, **kwargs):
        choice = request.POST.get('choice')
        option = Option.objects.get(id=choice)
        vote = Vote(user=self.request.user,
                    option_vote=option,
                    voting=self.get_object())

        return redirect('vote-list')

class VoteCreateView(LoginRequiredMixin, CreateView):
    pass



class VoteDeleteView(LoginRequiredMixin, UserIsOwnerMixins, DeleteView):
    pass