from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

# ✅ кастомний LogoutView з підтримкою GET
class CustomLogoutView(LogoutView):
    next_page = 'main:home'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path("gallery/", include("gallery.urls")),
    path("workshops/", include("workshops.urls")),
    path("casino/", include("casino.urls")),

    # accounts
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),

    # themes
    path("themes/", include(("themes.urls", "themes"), namespace="themes")),
]

# ✅ медіа тільки у DEBUG режимі
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
