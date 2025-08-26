from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden
from themes.models import Theme
from workshops.models import Workshop
from gallery.models import GalleryItem

from themes.models import Theme
from gallery.models import GalleryItem
from workshops.models import Workshop

from .forms import ThemeForm, WorkshopForm, GalleryItemForm

from  workshops.models import Workshop
from .forms import ThemeForm, WorkshopForm, GalleryItemForm

# THEMES
class ThemeListView(ListView):
    model = Theme
    template_name = 'workshops/theme_list.html'
    context_object_name = 'themes'


class ThemeCreateView(LoginRequiredMixin, CreateView):
    model = Theme
    form_class = ThemeForm
    template_name = 'workshops/theme_form.html'
    success_url = reverse_lazy('workshops:theme_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ThemeUpdateView(LoginRequiredMixin, UpdateView):
    model = Theme
    form_class = ThemeForm
    template_name = 'workshops/theme_form.html'
    success_url = reverse_lazy('workshops:theme_list')


class ThemeDeleteView(LoginRequiredMixin, DeleteView):
    model = Theme
    template_name = 'workshops/confirm_delete.html'
    success_url = reverse_lazy('workshops:theme_list')


# WORKSHOPS
class WorkshopListView(ListView):
    model = Workshop
    template_name = 'workshops/workshop_list.html'
    context_object_name = 'workshops'
    paginate_by = 12

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_published=True)


class WorkshopDetailView(DetailView):
    model = Workshop
    template_name = 'workshops/workshop_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class WorkshopCreateView(LoginRequiredMixin, CreateView):
    model = Workshop
    form_class = WorkshopForm
    template_name = 'workshops/workshop_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('workshops:workshop_detail', kwargs={'slug': self.object.slug})


class WorkshopUpdateView(LoginRequiredMixin, UpdateView):
    model = Workshop
    form_class = WorkshopForm
    template_name = 'workshops/workshop_form.html'

    def get_success_url(self):
        return reverse_lazy('workshops:workshop_detail', kwargs={'slug': self.object.slug})


class WorkshopDeleteView(LoginRequiredMixin, DeleteView):
    model = Workshop
    template_name = 'workshops/confirm_delete.html'
    success_url = reverse_lazy('workshops:workshop_list')


# GALLERY
class GalleryListView(ListView):
    model = GalleryItem
    template_name = 'workshops/gallery_list.html'
    context_object_name = 'items'
    paginate_by = 24

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return qs  # staff sees all
        return qs.filter(approved=True)


class GalleryCreateView(LoginRequiredMixin, CreateView):
    model = GalleryItem
    form_class = GalleryItemForm
    template_name = 'workshops/gallery_form.html'
    success_url = reverse_lazy('workshops:gallery_list')

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        form.instance.approved = False
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class GalleryModerationListView(ListView):
    model = GalleryItem
    template_name = 'workshops/gallery_moderation.html'
    context_object_name = 'items'
    paginate_by = 50

    def get_queryset(self):
        return GalleryItem.objects.filter(approved=False).order_by('created_at')


@staff_member_required
def approve_gallery_item(request, pk):
    item = get_object_or_404(GalleryItem, pk=pk)
    item.approved = True
    item.save(update_fields=['approved'])
    return redirect('workshops:gallery_moderation')


@staff_member_required
def delete_gallery_item(request, pk):
    item = get_object_or_404(GalleryItem, pk=pk)
    item.delete()
    return redirect('workshops:gallery_moderation')
