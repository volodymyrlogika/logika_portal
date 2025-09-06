import json
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Theme
from .forms import ThemeForm
from .utils import create_theme_css

@login_required
@csrf_exempt
def apply_theme(request, pk):
    if request.method == "POST":
        try:
            theme = Theme.objects.get(pk=pk)
            profile = request.user.profile
            profile.theme = theme.slug if hasattr(theme, "slug") else "light"
            profile.save()
            return JsonResponse({"success": True, "theme": profile.theme})
        except Theme.DoesNotExist:
            return JsonResponse({"success": False, "error": "Theme not found"}, status=404)
    return JsonResponse({"success": False, "error": "Invalid method"}, status=400)


class ThemeListView(ListView):
    model = Theme
    template_name = "themes/theme_list.html"
    context_object_name = "themes"


@login_required
@require_POST
def set_theme(request):
    """Встановлюємо тему для користувача"""
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "error": "Invalid JSON"}, status=400)

    theme = data.get("theme")
    if not theme:
        return JsonResponse({"status": "error", "error": "No theme provided"}, status=400)

    # ⚠️ НЕ викликаємо create_theme_css тут!
    request.session["theme"] = theme
    profile = request.user.profile
    profile.theme = theme
    profile.save()

    return JsonResponse({"status": "ok", "theme": theme})


@csrf_exempt
def theme_switch(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            theme = data.get("theme", "light")
        except Exception:
            return JsonResponse({"status": "error", "error": "Invalid JSON"}, status=400)
    elif request.method == "GET":
        theme = request.GET.get("theme", "light")
    else:
        return JsonResponse({"status": "error", "error": "Invalid request"}, status=405)

    # зберігаємо
    if request.user.is_authenticated:
        profile = request.user.profile
        profile.theme = theme
        profile.save()
    else:
        request.session["theme"] = theme

    # якщо GET → редірект назад
    if request.method == "GET":
        return redirect(request.META.get("HTTP_REFERER", "/"))

    return JsonResponse({"status": "ok", "theme": theme})


class ThemeListView(ListView):
    model = Theme
    template_name = "themes/theme_list.html"
    context_object_name = "themes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_slug = self.request.session.get("theme")
        if active_slug:
            context["active_theme"] = Theme.objects.filter(slug=active_slug).first()
        else:
            context["active_theme"] = Theme.objects.filter(is_active=True).first()
        return context


class ThemeDetailView(DetailView):
    model = Theme
    template_name = "themes/theme_detail.html"
    context_object_name = "theme"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_slug = self.request.session.get("theme")
        if active_slug:
            context["active_theme"] = Theme.objects.filter(slug=active_slug).first()
        else:
            context["active_theme"] = Theme.objects.filter(is_active=True).first()
        return context


class ThemeCreateView(CreateView):
    model = Theme
    form_class = ThemeForm
    template_name = "themes/theme_form.html"
    success_url = reverse_lazy("themes:theme_list")

    def form_valid(self, form):
        """Створення теми та генерація CSS"""
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user

        response = super().form_valid(form)

        # Генеруємо CSS тільки тут!
        create_theme_css(
            theme_name=form.instance.name,
            bg_color=form.instance.background_color,
            text_color=form.instance.text_color,
            extra_css=form.instance.custom_css or ""
        )

        return response

    def form_invalid(self, form):
        print("Form errors:", form.errors)
        return super().form_invalid(form)


class ThemeUpdateView(UpdateView):
    model = Theme
    form_class = ThemeForm
    template_name = "themes/theme_form.html"
    success_url = reverse_lazy("themes:theme_list")


class ThemeDeleteView(DeleteView):
    model = Theme
    template_name = "themes/theme_confirm_delete.html"
    success_url = reverse_lazy("themes:theme_list")
