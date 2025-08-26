from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('gallery/', include('gallery.urls')),
    # головна
    path("", include(("main.urls", "main"), namespace="main")),

    # акаунти
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),

    # воркшопи
    path("workshops/", include(("workshops.urls", "workshops"), namespace="workshops")),

    # галерея
    path("gallery/", include(("gallery.urls", "gallery"), namespace="gallery")),

    # теми
    path("themes/", include(("themes.urls", "themes"), namespace="themes")),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
