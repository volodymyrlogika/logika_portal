import os
from django.conf import settings

BASE_THEME_DIR = os.path.join(settings.BASE_DIR, "static", "css", "themes")

def create_theme_css(theme_name, bg_color="#ffffff", text_color="#000000", extra_css=""):
    os.makedirs(BASE_THEME_DIR, exist_ok=True)
    path = os.path.join(BASE_THEME_DIR, f"{theme_name}.css")

    css_content = f"""/* Автогенерація теми: {theme_name} */
body {{
    background-color: {bg_color};
    color: {text_color};
}}
.navbar, footer {{
    background-color: {bg_color};
    color: {text_color};
}}
{extra_css}
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(css_content)
    return path