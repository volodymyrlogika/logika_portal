from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from .models import GalleryItem
from .forms import GalleryItemForm


class GalleryListView(ListView):
    model = GalleryItem
    template_name = "gallery/gallery_list.html"
    context_object_name = "items"
    paginate_by = 12

    def get_queryset(self):
        tag = self.request.GET.get("tag")  # ?tag=назва_тегу
        if self.request.user.is_staff:
            queryset = GalleryItem.objects.all().order_by('-created_at')
        else:
            queryset = GalleryItem.objects.filter(status="approved").order_by('-created_at')

        if tag:
            queryset = queryset.filter(tags__name__iexact=tag)

        return queryset


class GalleryCreateView(LoginRequiredMixin, CreateView):
    model = GalleryItem
    form_class = GalleryItemForm
    template_name = "gallery/upload.html"
    success_url = reverse_lazy("gallery:home")

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super().form_valid(form)


class GalleryModerationListView(UserPassesTestMixin, ListView):
    model = GalleryItem
    template_name = "gallery/gallery_moderation.html"
    context_object_name = "items"

    def get_queryset(self):
        return GalleryItem.objects.filter(status="pending")

    def test_func(self):
        return self.request.user.is_staff


# --- функції для модерації ---
@user_passes_test(lambda u: u.is_staff)
def approve_gallery_item(request, pk):
    item = get_object_or_404(GalleryItem, pk=pk)
    item.status = 'approved'
    item.save(update_fields=['status'])
    messages.success(request, "Матеріал схвалено.")
    return redirect('gallery:moderation')


@user_passes_test(lambda u: u.is_staff)
def delete_gallery_item(request, pk):
    item = get_object_or_404(GalleryItem, pk=pk)
    item.delete()
    messages.success(request, "Матеріал видалено.")
    return redirect('gallery:moderation')
