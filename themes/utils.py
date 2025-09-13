# themes/utils.py
from pathlib import Path
from django.conf import settings
from django.utils.text import slugify


def _themes_dir() -> Path:
    """
    Повертає шлях до папки, де зберігати CSS теми:
    BASE_DIR/static/css/themes
    """
    return Path(settings.BASE_DIR) / "static" / "css" / "themes"


def create_theme_css(theme):
    """Генерує CSS файл для вибраної теми"""

    bg_image_css = ""
    if theme.background_image:
        if theme.background_mode == "cover":
            bg_image_css = f"""
            body {{
                background: url('{settings.MEDIA_URL}{theme.background_image.name}') center/cover no-repeat fixed;
            }}
            """
        elif theme.background_mode == "tile":
            bg_image_css = f"""
            body {{
                background: url('{settings.MEDIA_URL}{theme.background_image.name}') repeat;
            }}
            """
        elif theme.background_mode == "dim":
            bg_image_css = f"""
            body::before {{
                content: "";
                position: fixed;
                inset: 0;
                background: url('{settings.MEDIA_URL}{theme.background_image.name}') center/cover no-repeat;
                filter: brightness(0.5);
                z-index: -1;
            }}
            """

    css_content = f"""
    /* Автоматично згенерована тема: {theme.name} */
    body {{
        background-color: {theme.background_color};
       
        font-family: '{theme.font_family}', sans-serif;
    }}
    {bg_image_css}
    {theme.custom_css}
    """.strip()

    # папка для тем
    out_dir = _themes_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    # назва файлу за slug
    slug = slugify(theme.slug or theme.name)
    out_path = out_dir / f"{slug}.css"

    # запис у файл
    out_path.write_text(css_content, encoding="utf-8")

    return out_path
