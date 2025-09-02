from .models import Theme

def themes_context(request):
    themes = Theme.objects.all()  # прибрали is_draft
    active_theme = None
    theme_id = request.session.get("active_theme_id")
    if theme_id:
        active_theme = Theme.objects.filter(id=theme_id).first()
    else:
        active_theme = Theme.objects.filter().first()  # якщо хочеш брати першу доступну тему

    return {
        "themes_list": themes,
        "active_theme": active_theme
    }

def active_theme(request):
    slug = request.session.get("active_theme", "light")
    theme = Theme.objects.filter(slug=slug).first()
    return {"active_theme": theme}
def themes_dropdown(request):
    return {
        "all_themes": Theme.objects.all()
    }

def themes_list(request):
    return {
        "themes_list": Theme.objects.all(),
        "active_theme_slug": request.session.get("active_theme")
    }