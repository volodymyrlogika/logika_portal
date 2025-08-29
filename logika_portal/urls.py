from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

# ✅ кастомний LogoutView з підтримкою GET
class CustomLogoutView(LogoutView):
    next_page = 'main:home'
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


urlpatterns = [
    path("admin/", admin.site.urls),

    # головна
    path("", include(("main.urls", "main"), namespace="main")),

    # акаунти
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),

    # воркшопи
    path("workshops/", include(("workshops.urls", "workshops"), namespace="workshops")),

    # галерея
    path("gallery/", include(("gallery.urls", "gallery"), namespace="gallery")),

    # теми
    
    path("themes/", include("themes.urls")),
    path('casino/', include('casino.urls')),
    
    # логін / логаут
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="main:home"), name="logout"),
]

# Додаємо доступ до медіа тільки у режимі DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
