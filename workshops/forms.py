from django import forms
from .models import Workshop, GalleryItem


class WorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ["title", "description", "start_at", "location", "theme"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введіть назву воркшопу"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Короткий опис"}),
            "start_at": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "location": forms.TextInput(attrs={"class": "form-control", "placeholder": "Місце проведення"}),
            "theme": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        if request and request.GET.get("theme"):
            self.fields["theme"].widget = forms.HiddenInput()


class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ["title", "file", "media_type"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Назва файлу"}),
            "file": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "media_type": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_file(self):
        f = self.cleaned_data.get("file")
        if not f:
            return f

        allowed = (
            "image/png", "image/jpeg", "image/jpg", "image/webp", "image/gif",
            "video/mp4", "video/webm", "video/ogg", "video/quicktime"
        )

        if hasattr(f, "content_type") and f.content_type not in allowed:
            raise forms.ValidationError("Недопустимий тип файлу. Дозволені: зображення (png, jpg, gif, webp) або відео (mp4, webm, ogg, mov).")

        if f.size and f.size > 50 * 1024 * 1024:  # 50 MB
            raise forms.ValidationError("Файл завеликий (макс. 50MB).")

        return f

    def save(self, commit=True):
        instance = super().save(commit=False)
        file = self.cleaned_data.get("file")
        if file and hasattr(file, "content_type"):
            if file.content_type.startswith("image/"):
                instance.media_type = "image"
            elif file.content_type.startswith("video/"):
                instance.media_type = "video"
        if commit:
            instance.save()
        return instance
