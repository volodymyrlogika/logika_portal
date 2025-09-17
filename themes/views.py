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
from django.shortcuts import get_object_or_404, redirect

from .models import Theme
from .forms import ThemeForm
from .utils import create_theme_css
from workshops.models import Workshop  # ✅ To get workshop data


# ==========================
# API
# ==========================

@csrf_exempt
@require_POST
def set_theme(request: HttpRequest) -> JsonResponse:
    """Change theme via AJAX (by slug or id)"""
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
            return JsonResponse({"status": "error", "msg": "Theme not found"}, status=404)

        # ❌ Спочатку скидаємо активні теми користувача
        if request.user.is_authenticated:
            Theme.objects.filter(created_by=request.user, is_active=True).update(is_active=False)

        # ✅ Робимо поточну тему активною
        theme.is_active = True
        theme.save(update_fields=["is_active"])

        # Save in session
        request.session["active_theme"] = theme.slug

        return JsonResponse({
            "status": "ok",
            "slug": theme.slug,
            "css_url": f"/static/css/themes/{theme.slug}.css",
            "background_url": theme.background_image.url if theme.background_image else "",
        })

    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "msg": "Invalid JSON"}, status=400)
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

        # System themes
        context["system_themes"] = Theme.objects.filter(is_system=True)

        # User's custom themes
        if user.is_authenticated:
            context["user_themes"] = Theme.objects.filter(is_system=False, created_by=user)
        else:
            context["user_themes"] = Theme.objects.none()

        return context


class ThemeDetailView(DetailView):
    model = Theme
    template_name = "themes/theme_detail.html"
    context_object_name = "theme"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        active_slug = self.request.session.get("active_theme")

        context["active_theme"] = (
            Theme.objects.filter(slug=active_slug).first()
            if active_slug
            else Theme.objects.filter(is_active=True).first()
        )

        # Only system + user's custom themes
        user = self.request.user
        if user.is_authenticated:
            context["all_themes"] = Theme.objects.filter(is_system=True) | Theme.objects.filter(created_by=user, is_system=False)
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
            raise PermissionDenied("System themes cannot be edited.")
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
            raise PermissionDenied("System themes cannot be deleted.")
        return super().dispatch(request, *args, **kwargs)


# ==========================
# Create from Workshop
# ==========================

# themes/views.py
# themes/views.py
class ThemeFromWorkshopCreateView(LoginRequiredMixin, CreateView):
    model = Theme
    form_class = ThemeForm
    template_name = "themes/theme_form.html"
    success_url = reverse_lazy("themes:theme_list")

    def get(self, request, *args, **kwargs):
        workshop = get_object_or_404(Workshop, pk=self.kwargs["workshop_id"])

        base_name = workshop.title
        base_slug = slugify(base_name)
        name, slug, counter = base_name, base_slug, 1

        while Theme.objects.filter(name=name, created_by=request.user).exists() or Theme.objects.filter(slug=slug).exists():
            name = f"{base_name} ({counter})"
            slug = f"{base_slug}-{counter}"
            counter += 1

        # ❌ Скидаємо старі активні теми
        Theme.objects.filter(created_by=request.user, is_active=True).update(is_active=False)

        # ✅ Створюємо нову як активну
        theme = Theme.objects.create(
            name=name,
            description=workshop.description,
            slug=slug,
            created_by=request.user,
            is_system=False,
            is_active=True,   # <----
        )
        create_theme_css(theme)

        # зберігаємо slug у сесію
        request.session["active_theme"] = theme.slug

        return redirect(self.success_url)
