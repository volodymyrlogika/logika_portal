from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from themes.models import Theme


class Command(BaseCommand):
    help = "Створює стандартні системні теми (Light і Dark)"

    def handle(self, *args, **options):
        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            self.stdout.write(self.style.ERROR("Немає суперкористувача. Спершу створи суперюзера."))
            return

        themes_data = [
            {"name": "Light Theme", "slug": "light", "is_active": True},
            {"name": "Dark Theme", "slug": "dark", "is_active": False},
        ]

        for data in themes_data:
            theme, created = Theme.objects.get_or_create(
                slug=data["slug"],  # пошук по slug
                defaults={
                    "name": data["name"],
                    "created_by": admin,
                    "is_active": data["is_active"],
                    "is_system": True,   # ✅ важливе поле
                },
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Створено системну тему: {theme.name} ({theme.slug})")
                )
            else:
                # Якщо вже є, то можна примусово помітити як системну
                if not theme.is_system:
                    theme.is_system = True
                    theme.save(update_fields=["is_system"])
                    self.stdout.write(
                        self.style.WARNING(f"⚠️ Тема {theme.name} вже існувала, тепер позначено як системна")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"ℹ️ Тема {theme.name} ({theme.slug}) вже існує як системна")
                    )
