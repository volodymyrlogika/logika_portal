from django import forms
from .models import Workshop, GalleryItem
from themes.models import Theme  # ✅ додав імпорт



from django import forms
from .models import Workshop, GalleryItem


class WorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ["title", "description", "start_at", "location", "theme"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "start_at": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "theme": forms.Select(attrs={"class": "form-select"}),
        }


class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ["title", "file", "media_type"]
    
    def clean_file(self):
        f = self.cleaned_data.get('file')
        if not f:
            return f
        allowed = (
            'image/png','image/jpeg','image/jpg','image/webp','image/gif',
            'video/mp4','video/webm','video/ogg','video/quicktime'
        )
        if hasattr(f, 'content_type') and f.content_type not in allowed:
            raise forms.ValidationError('Недопустимий тип файлу. Дозволені зображення або відео.')
        if f.size and f.size > 50 * 1024 * 1024:
            raise forms.ValidationError('Файл завеликий (макс. 50MB).')
        return f
