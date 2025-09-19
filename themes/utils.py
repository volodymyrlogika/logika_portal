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
    if getattr(theme, "background_image", None):
        # якщо є поле background_mode → використовуємо його
        mode = getattr(theme, "background_mode", "cover")

        if mode == "cover":
            bg_image_css = f"""
            body {{
                background: url('{settings.MEDIA_URL}{theme.background_image.name}') center/cover no-repeat fixed;
            }}
            """
        elif mode == "tile":
            bg_image_css = f"""
            body {{
                background: url('{settings.MEDIA_URL}{theme.background_image.name}') repeat;
            }}
            """
        elif mode == "dim":
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
        else:
            # дефолт – як cover
            bg_image_css = f"""
            body {{
                background: url('{settings.MEDIA_URL}{theme.background_image.name}') center/cover no-repeat fixed;
            }}
            """

    css_content = f"""
    /* Автоматично згенерована тема: {theme.name} */
    body {{
        background-color: {getattr(theme, "background_color", "#ffffff")};
        font-family: '{getattr(theme, "font_family", "Arial")}', sans-serif;
        color: {getattr(theme, "text_color", "#000000")};
    }}
    {bg_image_css}
    {getattr(theme, "custom_css", "")}
    """.strip()

    # папка для тем
    out_dir = _themes_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    # назва файлу за slug
    slug = slugify(getattr(theme, "slug", None) or theme.name)
    out_path = out_dir / f"{slug}.css"

    # запис у файл
    out_path.write_text(css_content, encoding="utf-8")

    return out_path
