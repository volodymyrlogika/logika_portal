import json
from typing import Any, Dict

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from django.views.decorators.csrf import csrf_exempt
from .models import Theme
from .forms import ThemeForm
from .utils import create_theme_css


# ==========================
# API
# ==========================

@login_required
@require_POST
def apply_theme(request: HttpRequest, pk: int) -> JsonResponse:
    """Призначення теми користувачу"""
    try:
        theme: Theme = Theme.objects.get(pk=pk)
        profile = request.user.profile
        profile.theme = theme.slug if hasattr(theme, "slug") else "light"
        profile.save()
        return JsonResponse({"success": True, "theme": profile.theme})
    except Theme.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Theme not found"}, status=404
        )



@csrf_exempt
def set_theme(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            slug = data.get("theme")
            if not slug:
                return JsonResponse({"status": "error", "msg": "no theme provided"}, status=400)

            # шукаємо тему в БД
            theme = Theme.objects.filter(slug=slug).first()
            if not theme:
                return JsonResponse({"status": "error", "msg": f"theme {slug} not found"}, status=404)

            # зберігаємо slug у сесії
            request.session["active_theme"] = theme.slug

            return JsonResponse({
                "status": "ok",
                "slug": theme.slug,
                "css_url": f"/static/css/themes/{theme.slug}.css",
                "background_url": theme.background.url if theme.background else ""
            })

        except Exception as e:
            return JsonResponse({"status": "error", "msg": str(e)}, status=400)

    return JsonResponse({"status": "error", "msg": "only POST allowed"}, status=405)


# ==========================
# Views
# ==========================

class ThemeListView(ListView):
    model = Theme
    template_name = "themes/theme_list.html"
    context_object_name = "themes"


class ThemeDetailView(DetailView):
    model = Theme
    template_name = "themes/theme_detail.html"
    context_object_name = "theme"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        active_slug: str | None = self.request.session.get("theme")
        if active_slug:
            context["active_theme"] = Theme.objects.filter(slug=active_slug).first()
        else:
            context["active_theme"] = Theme.objects.filter(is_active=True).first()
        return context


class ThemeCreateView(LoginRequiredMixin, CreateView):
    model = Theme
    form_class = ThemeForm
    template_name = "themes/theme_form.html"
    success_url = reverse_lazy("themes:theme_list")

    def form_valid(self, form: ThemeForm):
        form.instance.slug = slugify(form.instance.slug or form.instance.name)
        response = super().form_valid(form)
        create_theme_css(self.object)  # генеруємо css
        return response

    def form_invalid(self, form: ThemeForm) -> HttpResponse:
        print("Form errors:", form.errors)
        return super().form_invalid(form)


class ThemeUpdateView(LoginRequiredMixin, UpdateView):
    model = Theme
    form_class = ThemeForm
    template_name = "themes/theme_form.html"
    success_url = reverse_lazy("themes:theme_list")

    def form_valid(self, form: ThemeForm):
        form.instance.slug = slugify(form.instance.slug or form.instance.name)
        response = super().form_valid(form)
        create_theme_css(self.object)  # оновлюємо CSS
        return response


class ThemeDeleteView(LoginRequiredMixin, DeleteView):
    model = Theme
    template_name = "themes/theme_confirm_delete.html"
    success_url = reverse_lazy("themes:theme_list")
