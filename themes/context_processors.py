from .models import Theme
from django.templatetags.static import static


def active_theme(request):
    active_slug = request.session.get("active_theme")

    theme = None
    if active_slug:
        theme = Theme.objects.filter(slug=active_slug, created_by=request.user).first()

    # fallback: активна тема юзера
    if not theme:
        theme = Theme.objects.filter(created_by=request.user, is_active=True).first()

    # fallback №2: системна дефолтна
    if not theme:
        theme = Theme.objects.filter(is_system=True).first()

    return {"active_theme": theme}


def themes_list(request):
    """Список усіх кастомних тем (для меню)"""
    return {"all_themes": Theme.objects.all()}
