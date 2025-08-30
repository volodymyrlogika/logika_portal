from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from accounts import views


from django.contrib.auth.views import LogoutView

# ✅ кастомний LogoutView з підтримкою GET
class CustomLogoutView(LogoutView):
    next_page = 'main:home'
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('accounts.urls')),
    path("gallery/", include("gallery.urls")),
    path("workshops/", include("workshops.urls")),
    path("themes/", include("themes.urls")),
    path("casino/", include("casino.urls")),
    path("accounts/", include("accounts.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

