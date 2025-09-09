from .models import Theme
from django.templatetags.static import static


def active_theme(request):
    active_slug = request.session.get("active_theme")
    if active_slug:
        theme = Theme.objects.filter(slug=active_slug).first()
    else:
        theme = Theme.objects.filter(is_active=True).first()
    return {"active_theme": theme}

def themes_list(request):
    """Список усіх кастомних тем (для меню)"""
    return {"all_themes": Theme.objects.all()}
