from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json

from .utils import create_theme_css
from .forms import ProfileForm, LoginForm, RegisterForm
from .models import Profile
from workshops.models import Workshop
from material.models import Material
from themes.models import Theme   # 🔹 Додано імпорт


# --------------------------
# Logout
# --------------------------
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')

    # Щоб кнопка "Вийти" могла використовувати GET
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


# --------------------------
# Застосування теми користувача через AJAX / POST
# --------------------------
@login_required
@require_POST
def set_theme(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "error": "Invalid JSON"}, status=400)

    theme = data.get("theme")
    if not theme:
        return JsonResponse({"status": "error", "error": "No theme provided"}, status=400)

    # Генеруємо CSS для нової теми
    request.session["theme"] = theme
    profile = request.user.profile
    profile.theme = theme
    profile.save()

    return JsonResponse({"status": "ok", "theme": theme})


# --------------------------
# Створення нової теми
# --------------------------
@login_required
def create_theme(request):
    if request.method == "POST":
        name = request.POST.get("name")
        bg = request.POST.get("bg_color", "#ffffff")
        text = request.POST.get("text_color", "#000000")
        extra_css = request.POST.get("extra_css", "")

        # зберегти тему в БД
        theme = Theme.objects.create(
            name=name,
            bg_color=bg,
            text_color=text,
            extra_css=extra_css
        )

        # створити CSS-файл
        create_theme_css(name, bg, text, extra_css)

        return redirect("themes:theme_list")

    return render(request, "themes/create_theme.html")  # 🔹 щоб GET не падав


# --------------------------
# Старий метод для сумісності
# --------------------------
@login_required
def set_session_theme(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            theme = data.get("theme", "light")
            if theme in ["light", "dark"]:
                request.session["theme"] = theme
                request.user.profile.theme = theme
                request.user.profile.save()
                return JsonResponse({"status": "ok", "theme": theme})
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "error": "Invalid JSON"}, status=400)
    return JsonResponse({"status": "error"}, status=400)


# --------------------------
# Профіль користувача
# --------------------------
@login_required
def profile_view(request, username=None):
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user

    profile = profile_user.profile
    workshops = Workshop.objects.filter(created_by=profile_user)
    materials = Material.objects.filter(creator=profile_user)

    return render(request, "accounts/profile.html", {
        "profile": profile,
        "profile_user": profile_user,
        "workshops": workshops,
        "materials": materials,
    })


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile", username=request.user.username)  # 🔹 виправлено редірект
    else:
        form = ProfileForm(instance=profile)

    return render(request, "accounts/edit_profile.html", {"form": form})


# --------------------------
# Логін / Логаут / Реєстрація
# --------------------------
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    form_class = LoginForm


class RegisterView(CreateView):
    model = User
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('accounts:login')


# --------------------------
# Відображення матеріалів
# --------------------------
@login_required
def material(request):
    materials = Material.objects.all()
    return render(request, 'material/material.html', {'materials': materials})
