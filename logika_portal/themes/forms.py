from django import forms
from logika_portal.themes.models import Theme, Workshop, GalleryItem

class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['name', 'description', 'background_color', 'text_color', 'custom_css']
        widgets = {
            'background_color': forms.TextInput(attrs={'type': 'color'}),
            'text_color': forms.TextInput(attrs={'type': 'color'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter description...'}),
            'custom_css': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Optional custom CSS...'}),
        }


class WorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = [
            "title",
            "description",
            "start_at",
            "end_at",
            "location",
            "capacity",
            "theme",
            "is_published",
        ]


class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ["title", "description", "file", "media_type", "workshop", "theme"]

    def clean_file(self):
        f = self.cleaned_data.get("file")
        if not f:
            return f
        allowed = (
            "image/png", "image/jpeg", "image/jpg", "image/webp", "image/gif",
            "video/mp4", "video/webm", "video/ogg", "video/quicktime"
        )
        if hasattr(f, "content_type") and f.content_type not in allowed:
            raise forms.ValidationError("Недопустимий тип файлу. Дозволені зображення або відео.")
        if f.size and f.size > 50 * 1024 * 1024:
            raise forms.ValidationError("Файл завеликий (макс. 50MB).")
        return f
