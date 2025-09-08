from .models import Theme
from django.templatetags.static import static


def active_theme(request):
    slug = request.session.get("theme", "light")
    try:
        theme = Theme.objects.get(slug=slug)
    except Theme.DoesNotExist:
        theme = None

    return {
        "active_theme": theme,
        "all_themes": Theme.objects.all()
    }

def themes_list(request):
    """Список усіх кастомних тем (для меню)"""
    return {"all_themes": Theme.objects.all()}
