# themes/utils.py
from pathlib import Path
from django.conf import settings
from django.utils.text import slugify


def _themes_dir() -> Path:
    """
    Повертає шлях до папки, де зберігати CSS теми:
    C:/Users/sypen/Downloads/portal/logika_portal/static/css/themes
    """
    return Path(settings.BASE_DIR) / "static" / "css" / "themes"


def create_theme_css(theme):
    """
    Генерує css для теми у вигляді файлу <slug>.css
    """
    slug = slugify(theme.slug or theme.name)

    css = f"""
/* ===== {theme.name} Theme Styles ===== */

body {{
  background-color: {theme.background_color} !important;
  color: {theme.text_color} !important;
}}

/* Navbar */
body[data-bs-theme="{slug}"] .navbar {{
  background-color: {theme.background_color} !important;
  color: {theme.text_color} !important;
}}

/* Footer */
body[data-bs-theme="{slug}"] footer {{
  background-color: {theme.background_color} !important;
  color: {theme.text_color} !important;
}}

/* Cards */
body[data-bs-theme="{slug}"] .card {{
  background-color: {theme.background_color} !important;
  color: {theme.text_color} !important;
  border-color: #2c2c2c !important;
}}

body[data-bs-theme="{slug}"] .card .card-title,
body[data-bs-theme="{slug}"] .card .card-text {{
  color: {theme.text_color} !important;
}}

/* Buttons */
body[data-bs-theme="{slug}"] .btn-primary {{
  background-color: #0d6efd;
  border-color: #0d6efd;
  color: #fff;
}}

body[data-bs-theme="{slug}"] .btn-success {{
  background-color: #198754;
  border-color: #198754;
  color: #fff;
}}

body[data-bs-theme="{slug}"] .btn-warning {{
  background-color: #ffc107;
  border-color: #ffc107;
  color: #212529;
}}

{theme.custom_css or ""}
    """.strip()

    out_dir = _themes_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{slug}.css"
    out_path.write_text(css, encoding="utf-8")
    return out_path
