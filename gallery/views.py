from django.views.generic import ListView, CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import GalleryItem
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

class GalleryListView(ListView):
    model = GalleryItem
    template_name = "gallery/gallery_list.html"
    context_object_name = "items"
    paginate_by = 12


class GalleryCreateView(LoginRequiredMixin, CreateView):
    model = GalleryItem
    fields = ["title", "caption", "file"]
    template_name = "gallery/upload.html"
    success_url = reverse_lazy("gallery:home")
    login_url = reverse_lazy("login")   # редірект на сторінку логіну

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super().form_valid(form)

class GalleryModerationListView(ListView):
    model = GalleryItem
    template_name = "gallery/gallery_moderation.html"
    context_object_name = "items"

    def get_queryset(self):
        return GalleryItem.objects.filter(status="pending")  # 👈 бо статус, а не approved


# --- функції для модерації ---
def approve_gallery_item(request, pk):
    item = get_object_or_404(GalleryItem, pk=pk)
    item.status = "approved"   # ✅ заміна is_approved
    item.save()
    return redirect("gallery:moderation")


def delete_gallery_item(request, pk):
    item = get_object_or_404(GalleryItem, pk=pk)
    item.delete()
    return redirect("gallery:moderation")
