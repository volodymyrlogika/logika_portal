from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Theme


class ThemeListView(ListView):
    model = Theme
    template_name = "themes/theme_list.html"
    context_object_name = "themes"


class ThemeDetailView(DetailView):
    model = Theme
    template_name = "themes/theme_detail.html"
    context_object_name = "theme"


class ThemeCreateView(CreateView):
    model = Theme
    template_name = "themes/theme_form.html"
    fields = ["name", "description"]  # ✅ зміни під свої поля
    success_url = reverse_lazy("themes:home")


class ThemeUpdateView(UpdateView):
    model = Theme
    template_name = "themes/theme_form.html"
    fields = ["name", "description"]
    success_url = reverse_lazy("themes:home")


class ThemeDeleteView(DeleteView):
    model = Theme
    template_name = "themes/theme_confirm_delete.html"
    success_url = reverse_lazy("themes:home")
