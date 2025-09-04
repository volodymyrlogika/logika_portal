# themes/utils.py
import os
from django.conf import settings

def create_theme_css(name, bg="#ffffff", text="#000000", extra_css="", font="Arial"):
    css_content = f"""
    body {{
        background-color: {bg};
        color: {text};
        font-family: '{font}', sans-serif;
    }}
    {extra_css}
    """

    themes_dir = os.path.join(settings.STATIC_ROOT, "css", "themes")
    os.makedirs(themes_dir, exist_ok=True)

    file_path = os.path.join(themes_dir, f"{name}.css")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(css_content)
