# themes/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from .models import Theme
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

# --- API для застосування теми ---
def set_theme(request, theme_id):
    theme = get_object_or_404(Theme, id=theme_id)
    request.session["active_theme_id"] = theme.id

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "slug": theme.slug,
            "css_url": theme.css_file.url if theme.css_file else ""
        })
    return redirect(request.META.get("HTTP_REFERER", "/"))

# --- Список тем ---
class ThemeListView(ListView):
    model = Theme
    template_name = "themes/theme_list.html"
    context_object_name = "themes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_id = self.request.session.get("active_theme_id")
        if active_id:
            context["active_theme"] = Theme.objects.filter(id=active_id).first()
        else:
            context["active_theme"] = Theme.objects.filter(is_active=True).first()
        return context


# --- Деталі теми ---
class ThemeDetailView(DetailView):
    model = Theme
    template_name = "themes/theme_detail.html"
    context_object_name = "theme"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_id = self.request.session.get("active_theme_id")
        if active_id:
            context["active_theme"] = Theme.objects.filter(id=active_id).first()
        else:
            context["active_theme"] = Theme.objects.filter(is_active=True).first()
        return context


# --- CRUD ---
class ThemeCreateView(CreateView):
    model = Theme
    template_name = "themes/theme_form.html"
    fields = ["name", "description", "image", "tags"]
    success_url = reverse_lazy("themes:list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ThemeUpdateView(UpdateView):
    model = Theme
    template_name = "themes/theme_form.html"
    fields = ["name", "description", "image", "tags"]
    success_url = reverse_lazy("themes:list")


class ThemeDeleteView(DeleteView):
    model = Theme
    template_name = "themes/theme_confirm_delete.html"
    success_url = reverse_lazy("themes:list")
