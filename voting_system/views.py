from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.transaction import commit
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView

from voting_system.forms import CreateVotingForm
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

#створення голосування
@login_required
def create_voting(request):
    form = CreateVotingForm()

    if request.method == 'POST':
        form = CreateVotingForm(request.POST)
        if form.is_valid():
            voting_create = Voting.objects.create(name=form.cleaned_data['name'],
                                  data_start=form.cleaned_data['data_start'],
                                  data_end=form.cleaned_data['data_end'],
                                  author=request.user)

            Option.objects.create(name=form.cleaned_data['option_1'],
                                  voting=voting_create).save()

            Option.objects.create(name=form.cleaned_data['option_2'],
                                  voting=voting_create).save()

            voting_create.save()
            return redirect('vote-list')

    context = {
        'form': form,
    }
    return render(request, template_name='voting_system/voting_form.html', context=context)

class VoteDeleteView(LoginRequiredMixin, DeleteView, UserIsOwnerMixins):
    model = Voting
    success_url = reverse_lazy('vote-list')
    template_name = 'voting_system/vote_delete_confirmation.html'