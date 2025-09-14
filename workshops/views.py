from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Workshop
from .forms import WorkshopForm


def page(request):
    return render(request, "workshops/page.html")


def workshop_page(request):
    return render(request, "workshops/page.html")


class WorkshopListView(ListView):
    model = Workshop
    template_name = "workshops/workshop_list.html"  # ✅ правильний шаблон
    context_object_name = "workshops"

    def get_queryset(self):
        return Workshop.objects.filter(is_published=True).select_related("theme", "created_by")


class WorkshopDetailView(DetailView):
    model = Workshop
    template_name = "workshops/detail.html"
    context_object_name = "workshop"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class WorkshopCreateView(LoginRequiredMixin, CreateView):
    model = Workshop
    form_class = WorkshopForm
    template_name = "workshops/form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request  # передаємо request у форму
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        theme_id = self.request.GET.get("theme")
        if theme_id:
            initial["theme"] = theme_id
        return initial

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("workshops:detail", kwargs={"slug": self.object.slug})


@login_required
def publish_workshop(request, pk):
    workshop = get_object_or_404(Workshop, pk=pk, created_by=request.user)
    workshop.publish()
    return redirect("workshops:detail", slug=workshop.slug)
