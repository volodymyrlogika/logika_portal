import json
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Theme
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


# --- API для застосування теми ---
@csrf_exempt
def set_theme(request):
    if request.user.is_authenticated and request.method == "POST":
        data = json.loads(request.body)
        theme = data.get("theme", "light")
        request.user.profile.theme = theme
        request.user.profile.save()
        return JsonResponse({"status": "ok", "theme": theme})
    return JsonResponse({"status": "error"}, status=400)


def switch_theme(request, slug):
    theme = get_object_or_404(Theme, slug=slug)
    request.session["theme"] = theme.slug  # зберігаємо у session

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "css_url": theme.css_file.url if theme.css_file else f"/static/css/themes/{theme.slug}.css"
        })
    return redirect("themes:list")


# --- Список тем ---
class ThemeListView(ListView):
    model = Theme
    template_name = "themes/theme_list.html"
    context_object_name = "themes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_slug = self.request.session.get("theme")  # уніфіковано
        if active_slug:
            context["active_theme"] = Theme.objects.filter(slug=active_slug).first()
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
        active_slug = self.request.session.get("theme")  # тепер теж "theme"
        if active_slug:
            context["active_theme"] = Theme.objects.filter(slug=active_slug).first()
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
        if self.request.user.is_authenticated:
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
