from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from themes.models import Theme


class Command(BaseCommand):
    help = "Створює стандартні теми (Light і Dark)"

    def handle(self, *args, **options):
        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            self.stdout.write(self.style.ERROR("Немає суперкористувача. Спершу створи суперюзера."))
            return

        themes_data = [
            {"name": "Light Theme", "slug": "light", "description": "Світла тема", "is_active": True},
            {"name": "Dark Theme", "slug": "dark", "description": "Темна тема", "is_active": False},
        ]

        for data in themes_data:
            theme, created = Theme.objects.get_or_create(
                slug=data["slug"],   # ✅ тепер пошук по slug
                defaults={
                    "name": data["name"],
                    "description": data["description"],
                    "created_by": admin,
                    "is_active": data["is_active"],
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Створено тему: {theme.name} ({theme.slug})"))
            else:
                self.stdout.write(self.style.WARNING(f"Тема {theme.name} ({theme.slug}) вже існує"))
