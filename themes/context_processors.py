from .models import Theme

def themes_context(request):
    themes = Theme.objects.filter(is_draft=False)
    active_theme = None
    theme_id = request.session.get("active_theme_id")
    if theme_id:
        active_theme = Theme.objects.filter(id=theme_id).first()
    else:
        active_theme = Theme.objects.filter(is_active=True).first()

    return {
        "themes_list": themes,
        "active_theme": active_theme
    }
