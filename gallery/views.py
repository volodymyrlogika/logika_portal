from django.views.generic import ListView, CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import GalleryItem


class GalleryListView(ListView):
    model = GalleryItem
    template_name = "gallery/gallery_list.html"  # створи цей шаблон
    context_object_name = "items"
    paginate_by = 12  # наприклад, по 12 картинок на сторінку


class GalleryCreateView(CreateView):
    model = GalleryItem
    template_name = "gallery/gallery_form.html"
    fields = ["image", "caption"]
    success_url = reverse_lazy("gallery:home")

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super().form_valid(form)


class GalleryModerationListView(ListView):
    model = GalleryItem
    template_name = "gallery/gallery_moderation.html"
    context_object_name = "items"

    def get_queryset(self):
        return GalleryItem.objects.filter(approved=False)


# --- функції для модерації ---
def approve_gallery_item(request, pk):
    item = GalleryItem.objects.get(pk=pk)
    item.approved = True
    item.save()
    return redirect("gallery:gallery_moderation")


def delete_gallery_item(request, pk):
    item = GalleryItem.objects.get(pk=pk)
    item.delete()
    return redirect("gallery:gallery_moderation")
