from themes.models import Theme

def themes_context(request):
    themes = Theme.objects.all()
    active_theme = request.session.get("active_theme_id")

    return {
        "themes_list": themes,
        "active_theme": Theme.objects.filter(id=active_theme).first() if active_theme else None
    }
