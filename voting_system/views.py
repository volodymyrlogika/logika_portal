from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView

from voting_system.forms import VotingForm
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
                    voting=self.get_object()).save()

        return redirect('vote-list')


class VoteCreateView(LoginRequiredMixin, CreateView):
    model = Voting
    template_name = 'voting_system/voting_form.html'
    form_class = VotingForm
    success_url = reverse_lazy('vote-list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

class VoteDeleteView(LoginRequiredMixin, DeleteView, UserIsOwnerMixins):
    model = Voting
    success_url = reverse_lazy('vote-list')
    template_name = 'voting_system/vote_delete_confirmation.html'