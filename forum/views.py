from django.shortcuts import render, redirect
from .models import Post, Thread, Category
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class CategoryListView(ListView):
    model = Category
    context_object_name = "categories"
    template_name = "forum/category_list.html"

class CategoryMixin:
    def get_categories(self):
        return Category.objects.all()

class ThreadListView(ListView):
    model = Thread
    context_object_name = "threds"
    template_name = "forum/thread_list.html"

class ThreadMixin:
    def get_threads(self):
        return Thread.objects.all()

class ForumHomeView(ThreadMixin, CategoryMixin, TemplateView):
    template_name="forum/forum_home.html"



    def get_context_data(self, *args, **kwargs):

        context = super().get_context_data(**kwargs)
        context['categories'] = self.get_categories()
        context['threads'] = self.get_threads()
        return context
