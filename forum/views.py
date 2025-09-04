from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Thread, Category
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from forum import models
from forum.forms import PostForm

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
        return Thread.objects.filter(category_id=self.kwargs['category_id'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs['category_id']
        return context

# class PostCreateView(CreateView):
#     model = Post
#     template_name = 

class PostList(ListView):
    model = models.Post
    context_object_name = "posts"
    template_name = "forum/post_list.html"
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm()
        context['category_id'] = self.kwargs['category_id']
        context['thread_id'] = self.kwargs['thread_id']
        return context
    
    def get_queryset(self):
        context = Post.objects.filter(
            url_category_id=self.kwargs['category_id'],
            url_thread_id=self.kwargs['thread_id'])
        return context
    
    def post(self, request, *args, **kwargs):
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user

            thread_id = self.kwargs.get("thread_id")
            category_id = self.kwargs.get("category_id")

            # thread_id = get_object_or_404(Thread, pk=thread_id)

            thread = get_object_or_404(Thread, pk=thread_id) 
            ######################
            post.thread = thread#############ці 2 рядка мені допоміг gpt бо я не міг зрозмуіти чому помилка потім розберусь 
            post.url_thread_id = thread.id###
            ########################3#
            
            post.url_category_id = category_id
            post.url_thread_id = thread_id

            
            post.save()
            return redirect('forum:post-list',category_id=category_id, thread_id=thread_id)
        else:
            pass