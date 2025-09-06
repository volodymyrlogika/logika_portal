from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Announcement

# Міксин: доступ тільки для адмінів і модераторів
class ModeratorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.groups.filter(name="модератор").exists()

# Список оголошень
class AnnouncementListView(ListView):
    model = Announcement
    template_name = "announcements/list.html"
    context_object_name = "announcements"

    def get_queryset(self):
        return Announcement.objects.filter(is_published=True)

# Деталі оголошення
class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = "announcements/detail.html"
    context_object_name = "announcement"

# Створення
class AnnouncementCreateView(ModeratorRequiredMixin, CreateView):
    model = Announcement
    fields = ["title", "content", "is_published"]
    template_name = "announcements/form.html"
    success_url = reverse_lazy("announcement_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Редагування
class AnnouncementUpdateView(ModeratorRequiredMixin, UpdateView):
    model = Announcement
    fields = ["title", "content", "is_published"]
    template_name = "announcements/form.html"
    success_url = reverse_lazy("announcement_list")

# Видалення
class AnnouncementDeleteView(ModeratorRequiredMixin, DeleteView):
    model = Announcement
    template_name = "announcements/confirm_delete.html"
    success_url = reverse_lazy("announcement_list")

