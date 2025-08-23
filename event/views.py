from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
# Create your views here.
class EventListView(ListView):
    model = Event
    template_name = 'calendar.html'
    context_object_name = 'events'

class EventCreateView(CreateView):
    model = Event
    template_name = 'calendar-create.html'
    fields = ['title', 'description', 'date', 'speciality', 'user']


class EventUpdateView()