import json
from typing import Any, Dict

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied

from .models import Theme
from .forms import ThemeForm
from .utils import create_theme_css


# ==========================
# API
# ==========================

@csrf_exempt
@require_POST
def set_theme(request: HttpRequest) -> JsonResponse:
    """Зміна теми через AJAX (по slug або id)"""
    try:
        data = json.loads(request.body.decode("utf-8"))

        slug = data.get("theme")
        theme_id = data.get("theme_id")

        theme = None
        if slug:
            theme = Theme.objects.filter(slug=slug).first()
        elif theme_id:
            theme = Theme.objects.filter(pk=theme_id).first()

        if not theme:
            return JsonResponse({"status": "error", "msg": "theme not found"}, status=404)

        # зберігаємо в сесію
        request.session["active_theme"] = theme.slug

        return JsonResponse({
            "status": "ok",
            "slug": theme.slug,
            "css_url": f"/static/css/themes/{theme.slug}.css",
            "background_url": theme.background_image.url if theme.background_image else "",
            "background_mode": getattr(theme, "background_mode", "cover"),
        })

    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "msg": "invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "msg": str(e)}, status=400)


# ==========================
# Views
# ==========================

class ThemeListView(ListView):
    model = Theme
    template_name = "themes/theme_list.html"
    context_object_name = "themes"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Системні теми
        context["system_themes"] = Theme.objects.filter(is_system=True)

        # Кастомні теми користувача
        if user.is_authenticated:
            context["user_themes"] = Theme.objects.filter(is_system=False, created_by=user)
        else:
            context["user_themes"] = []

        return context


class ThemeDetailView(DetailView):
    model = Theme
    template_name = "themes/theme_detail.html"
    context_object_name = "theme"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        active_slug = self.request.session.get("active_theme")

        if active_slug:
            context["active_theme"] = Theme.objects.filter(slug=active_slug).first()
        else:
            context["active_theme"] = Theme.objects.filter(is_active=True).first()

        # тільки системні + мої кастомні
        if self.request.user.is_authenticated:
            context["all_themes"] = (
                Theme.objects.filter(is_system=True)
                | Theme.objects.filter(created_by=self.request.user, is_system=False)
            )
        else:
            context["all_themes"] = Theme.objects.filter(is_system=True)

        return context


class ThemeCreateView(LoginRequiredMixin, CreateView):
    model = Theme
    form_class = ThemeForm
    template_name = "themes/theme_form.html"
    success_url = reverse_lazy("themes:theme_list")

    def form_valid(self, form: ThemeForm):
        form.instance.slug = slugify(form.instance.slug or form.instance.name)
        form.instance.created_by = self.request.user
        form.instance.is_system = False
        response = super().form_valid(form)
        create_theme_css(self.object)
        return response


class ThemeUpdateView(LoginRequiredMixin, UpdateView):
    model = Theme
    form_class = ThemeForm
    template_name = "themes/theme_form.html"
    success_url = reverse_lazy("themes:theme_list")

    def dispatch(self, request, *args, **kwargs):
        theme = self.get_object()
        if theme.is_system:
            raise PermissionDenied("Системні теми не можна редагувати.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: ThemeForm):
        form.instance.slug = slugify(form.instance.slug or form.instance.name)
        response = super().form_valid(form)
        create_theme_css(self.object)
        return response


class ThemeDeleteView(LoginRequiredMixin, DeleteView):
    model = Theme
    template_name = "themes/theme_confirm_delete.html"
    success_url = reverse_lazy("themes:theme_list")

    def dispatch(self, request, *args, **kwargs):
        theme = self.get_object()
        if theme.is_system:
            raise PermissionDenied("Системні теми не можна видаляти.")
        return super().dispatch(request, *args, **kwargs)
