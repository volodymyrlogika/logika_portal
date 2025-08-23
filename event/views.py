from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event

# Create your views here.
class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'calendar.html'
    context_object_name = 'events'


class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    template_name = 'calendar-create.html'
    fields = ['title', 'description', 'date', 'speciality']
    success_url = reverse_lazy('calendar')


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    template_name = 'calendar-update.html'
    fields = ['title', 'description', 'date', 'speciality']
    success_url = reverse_lazy('calendar')

class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'calendar-delete.html'
    success_url = reverse_lazy('calendar')