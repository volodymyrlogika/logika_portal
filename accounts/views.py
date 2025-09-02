from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from .forms import ProfileForm, LoginForm, RegisterForm
from .models import Profile
from workshops.models import Workshop
from material.models import Material
class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
@csrf_exempt
@login_required
def set_theme(request):
    """
    AJAX / POST для застосування теми користувача.
    URL: accounts/set_theme/
    """
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
# AJAX / POST для теми
# --------------------------
@csrf_exempt
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
        user = get_object_or_404(User, username=username)
    else:
        user = request.user

    profile = user.profile
    workshops = Workshop.objects.filter(created_by=user)
    materials = Material.objects.filter(creator=user)

    return render(request, "accounts/profile.html", {
        "profile": profile,
        "user": user,
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
            return redirect("accounts:profile")  # редірект після збереження
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

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')

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
