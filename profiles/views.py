from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm

@login_required
def profile_view(request):
    return render(request, "profiles/profile.html")

@login_required
def settings_view(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            # збереження теми
            theme = form.cleaned_data.get("theme")
            if theme:
                request.user.profile.theme = theme.slug
                request.user.profile.save()
                request.session["theme"] = theme.slug
            return redirect("profiles:profile")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "profiles/settings.html", {"form": form})
