from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from accounts.forms import LoginForm, RegisterForm
from .forms import ProfileForm
from .models import Profile
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from material.models import Material


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html")


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "accounts/edit_profile.html", {"form": form})


@login_required
def set_theme(request):
    theme = request.GET.get("theme", "light")
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile.theme = theme
    profile.save()
    return JsonResponse({"status": "ok", "theme": profile.theme})


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


def material(request):
    materials = Material.objects.all()
    return render(request, 'material/material.html', {'materials': materials})
