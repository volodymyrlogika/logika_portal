from .models import Theme

def active_theme(request):
    active_slug = request.session.get("active_theme")

    theme = None
    if active_slug:
        theme = Theme.objects.filter(slug=active_slug).first()

    if not theme:
        theme = Theme.objects.filter(is_active=True).first()

    if not theme:
        theme = Theme.objects.filter(is_system=True).first()

    return {"active_theme": theme}


def themes_list(request):
    """Список усіх тем (для меню)"""
    return {"all_themes": Theme.objects.all()}
