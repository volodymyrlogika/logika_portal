from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Thread, Category
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from forum import models
from forum.forms import PostForm, ThreadForm
from django.urls import reverse_lazy


class AllCategoryListView(LoginRequiredMixin,ListView):
    model = Category
    context_object_name = "categories"
    template_name = "forum/category_list.html"

class CategoryMixin:
    def get_categories(self):
        return Category.objects.all()

class AllThreadListView(LoginRequiredMixin,ListView):
    model = Thread
    context_object_name = "threds"
    template_name = "forum/all_thread_list.html"


class ThreadMixin:
    def get_threads(self):
        return Thread.objects.all()

class ForumHomeView(LoginRequiredMixin, ThreadMixin, CategoryMixin, TemplateView):
    template_name="forum/forum_home.html"



    def get_context_data(self, *args, **kwargs):

        context = super().get_context_data(**kwargs)
        context['categories'] = self.get_categories()
        context['threads'] = self.get_threads()
        return context
#########################################

class ThreadListView(LoginRequiredMixin, ListView):
    model = Thread
    context_object_name = "threads"
    template_name = "forum/thread_list.html"

    def get_queryset(self):
        return Thread.objects.filter(category_id=self.kwargs['category_id'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs['category_id']
        context['status'] = self.create_thread_button()
        return context
    
    def create_thread_button(self):
            user = self.request.user
            if user.is_staff:
                status = True
            elif user.is_superuser:
                status = True
            else:
                status = False
            return status
    
class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = models.Thread
    template_name = "forum/thread_create.html"
    form_class = ThreadForm
    success_url = ("http://127.0.0.1:8000/forum/home/")

    def form_valid(self, form):
        form.instance.author = self.request.user
        
        
        return super().form_valid(form)

# class PostCreateView(CreateView):
#     model = Post
#     template_name = 

class PostList(LoginRequiredMixin,ListView):
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
            
            post.thread = thread
            
            post.url_category_id = category_id
            post.url_thread_id = thread.id

            
            post.save()
            # return redirect('forum:post-list')
            return redirect('forum:post-list',category_id=category_id, thread_id=thread_id)
        else:
            pass