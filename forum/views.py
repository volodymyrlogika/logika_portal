from django.shortcuts import render, redirect
from .models import Post, Thread, Category
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from forum import models

class AllCategoryListView(ListView):
    model = Category
    context_object_name = "categories"
    template_name = "forum/category_list.html"

class CategoryMixin:
    def get_categories(self):
        return Category.objects.all()

class AllThreadListView(ListView):
    model = Thread
    context_object_name = "threds"
    template_name = "forum/all_thread_list.html"

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
#########################################

class ThreadListView(ListView):
    model = Thread
    context_object_name = "threads"
    template_name = "thread_list.html"

    def get_queryset(self):
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs['category_id']
        return context

class PostList(ListView):
    model = models.Post
    context_object_name = "posts"
    template_name = "forum/post_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs['category_id']
        context['thread_id'] = self.kwargs['thread_id']
        return context