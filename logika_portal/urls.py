from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# ✅ кастомний LogoutView з підтримкою GET
class CustomLogoutView(LogoutView):
    next_page = 'main:home'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

# ✅ кастомна реєстрація
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # після реєстрації → на логін
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path("gallery/", include("gallery.urls")),
    path("workshops/", include("workshops.urls")),
    path("casino/", include("casino.urls")),

    # accounts
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("accounts/", include("django.contrib.auth.urls")),
    path('logout/', CustomLogoutView.as_view(next_page='main:home'), name='logout'),

    # themes
    path("themes/", include(("themes.urls", "themes"), namespace="themes")),

    # ✅ реєстрація
    path("accounts/register/", register_view, name="register"),
]

# ✅ медіа тільки у DEBUG режимі
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
