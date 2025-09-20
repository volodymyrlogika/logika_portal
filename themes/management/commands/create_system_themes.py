from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from themes.models import Theme
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Створює стандартні системні теми (Light і Dark)"

    def handle(self, *args, **options):
        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            self.stdout.write(self.style.ERROR("❌ Немає суперкористувача. Спершу створи суперюзера."))
            return

        themes_data = [
            {
                "name": "Light Theme",
                "slug": "light",
                "is_active": True,
                "css_file": "css/themes/light.css",
            },
            {
                "name": "Dark Theme",
                "slug": "dark",
                "is_active": False,
                "css_file": "css/themes/dark.css",
            },
        ]

        for data in themes_data:
            theme, created = Theme.objects.get_or_create(
                slug=data["slug"],
                defaults={
                    "name": data["name"],
                    "created_by": admin,
                    "is_active": data["is_active"],
                    "is_system": True,
                },
            )

            if not created:
                # оновлюємо існуючу
                theme.name = data["name"]
                theme.is_system = True
                theme.created_by = admin
                theme.is_active = data["is_active"]
            theme.slug = slugify(data["slug"])
            theme.css_file = data["css_file"]
            theme.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Створено системну тему: {theme.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"ℹ️ Оновлено системну тему: {theme.name}"))

        # Робимо так, щоб лише одна системна була активна
        active_theme = Theme.objects.filter(is_system=True, is_active=True).first()
        if active_theme:
            Theme.objects.filter(is_system=True).exclude(pk=active_theme.pk).update(is_active=False)
            self.stdout.write(self.style.SUCCESS(f"🔄 Активна системна тема: {active_theme.name}"))
