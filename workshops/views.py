from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.generic import DetailView, CreateView, ListView
from django.urls import reverse_lazy
from django import forms

from .models import Workshop
from .forms import WorkshopForm


def page(request):
    return render(request, "workshops/page.html")


def workshop_page(request):
    return render(request, "workshops/page.html")


class WorkshopListView(ListView):
    model = Workshop
    template_name = "workshops/list.html"
    context_object_name = "workshops"

    def get_queryset(self):
        # Показуємо тільки опубліковані воркшопи
        return Workshop.objects.filter(is_published=True).select_related("theme", "created_by")


class WorkshopDetailView(DetailView):
    model = Workshop
    template_name = "workshops/detail.html"
    context_object_name = "workshop"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class WorkshopCreateView(CreateView):
    model = Workshop
    form_class = WorkshopForm
    template_name = "workshops/form.html"
    success_url = reverse_lazy("workshops:list")  # перенаправляємо на список

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        theme_id = self.request.GET.get("theme")
        if theme_id:
            form.fields["theme"].widget = forms.HiddenInput()
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        theme_id = self.request.GET.get("theme")
        if theme_id:
            form.instance.theme_id = theme_id
        return super().form_valid(form)


@login_required
def publish_workshop(request, pk):
    workshop = get_object_or_404(Workshop, pk=pk)

    if workshop.created_by != request.user:
        return HttpResponseForbidden("Ви не можете опублікувати цей воркшоп")

    workshop.is_published = True
    workshop.save()

    return redirect("workshops:detail", pk=workshop.pk)
