from . import forms
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
import calendar
from datetime import date
from collections import defaultdict

from .models import Event

# Create your views here.
class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'calendar/calendar.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.EventFilterForm()
        today = date.today()
        cal = calendar.Calendar(firstweekday=0)  # Monday
        month_days = cal.monthdayscalendar(today.year, today.month)
        context['month_days'] = month_days
        context['month_name'] = today.strftime('%B')
        context['year'] = today.year

        # Build a mapping: day -> list of events
        events_by_day = defaultdict(list)
        for event in Event.objects.filter(user=self.request.user, date__year=today.year, date__month=today.month):
            events_by_day[event.date.day].append(event)
        context['events_by_day'] = events_by_day
        return context
    
    def get_queryset(self):
        queryset = Event.objects.filter(user=self.request.user)
        speciality = self.request.GET.get('speciality')
        if speciality:
            queryset = queryset.filter(speciality=speciality)
        return queryset

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = forms.EventForm
    template_name = 'calendar/calendar-create.html'
    success_url = reverse_lazy('calendar')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    template_name = 'calendar/calendar-update.html'
    fields = ['title', 'description', 'date', 'speciality']
    success_url = reverse_lazy('calendar')


class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'calendar/calendar-delete.html'
    success_url = reverse_lazy('calendar')
#ахах удали ето нахуй если надо)
#ladno ne nado