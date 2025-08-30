from django.shortcuts import render
from .models import Post, Thread, Category
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

class ForumHomeView():
    pass

class CategoryListView(ListView):
    model = Category
    context_object_name = "categories"
    template_name = "forum/category_list.html"

class ThreadListView(ListView):
    pass
    