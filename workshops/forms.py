from django import forms
from themes.models import Theme, Workshop, GalleryItem

class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['name', 'description']

class WorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ['title', 'description', 'start_at', 'end_at', 'location', 'capacity', 'theme', 'is_published']

class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ['title', 'caption', 'file']



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
