from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Thread, Category, ReplyPost
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from forum import models
from forum.forms import PostForm, ThreadForm, ReplyPostForm
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator

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

class СheckUserAdminMixin:
    def create_thread_button(self):
            user = self.request.user
            if user.is_staff:
                status = True
            elif user.is_superuser:
                status = True
            else:
                status = False
            return status
    
class ThreadListView(LoginRequiredMixin, ListView, СheckUserAdminMixin):
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
    
    

class ThreadCreateView(LoginRequiredMixin, CreateView, СheckUserAdminMixin):
    model = models.Thread
    template_name = "forum/thread_create.html"
    form_class = ThreadForm
    # success_url = ("forum/home/")

    def form_valid(self, form, *args, **kwargs):
        form.instance.author = self.request.user
        status = self.create_thread_button()###викликаєм перевірк статус
        category_id = self.kwargs["category_id"]      # пдіставляє м url
        form.instance.category_id = category_id ## без цього не юуде працювати


        if status == True:
            valid = super().form_valid(form)
            return valid
        else:
            print("form invalid")
            valid = super().form_invalid(form)

            return valid

    def get_success_url(self, *args, **kwargs):
        category_id = self.kwargs.get("category_id")
        return reverse_lazy("forum:thread-list", kwargs={"category_id": category_id}) ####то мені чот гпт підказав бо я хз чо варіант занизу не преренаправляв
        # return reverse_lazy("forum:thread-list", category_id = category_id)

class ThreadDeleteView(LoginRequiredMixin, DeleteView):
    model = Thread
    template_name = "forum/thread_delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "forum:thread-list",
        kwargs={
            "category_id": self.kwargs["category_id"],
        },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs['category_id']
        return context

class ThreadUpdateView(LoginRequiredMixin, UpdateView):
    model = Thread
    form_class = ThreadForm
    template_name = "forum/thread_update.html"

    def get_success_url(self):
        return reverse_lazy(
            "forum:thread-list",
            kwargs={
                "category_id":self.kwargs["category_id"],
            }
        )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs['category_id']
        return context
    
class PostList(LoginRequiredMixin,ListView):
    model = models.Post
    context_object_name = "posts"
    template_name = "forum/post_list.html"
    form_class = PostForm
    paginate_by = 3
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_form"] = PostForm()
        context['reply_form'] = ReplyPostForm()
        context['category_id'] = self.kwargs['category_id']
        context['thread_id'] = self.kwargs['thread_id']
        return context
    
    def get_queryset(self):
        context = Post.objects.filter(
            url_category_id=self.kwargs['category_id'],
            url_thread_id=self.kwargs['thread_id'])
        return context
    
    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        # post_form = PostForm(request.POST, request.FILES)
        # reply_form = ReplyPostForm(request.POST, request.FILES)
        if action == "cookies":
            request.session['username'] = 'pipi'
            return self.get(request, *args, **kwargs)
        else:
            pass

    
        if action == "reply":
            reply_form = ReplyPostForm(request.POST, request.FILES)
            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.author = request.user
                post_id = request.POST.get("post_id")
                if post_id:
                    post = get_object_or_404(Post, id=post_id)
                    reply.post = post
                    reply.save()
                thread_id = self.kwargs.get("thread_id")
                category_id = self.kwargs.get("category_id")
                return redirect('forum:post-list',category_id=category_id, thread_id=thread_id)
            else:
                pass

        elif action == "post":
            post_form = PostForm(request.POST, request.FILES)

            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.author = request.user
                thread_id = self.kwargs.get("thread_id")
                category_id = self.kwargs.get("category_id")
                thread = get_object_or_404(Thread, pk=thread_id) 
                post.thread = thread
                post.url_category_id = category_id
                post.url_thread_id = thread.id
                post.save()

                return redirect('forum:post-list',category_id=category_id, thread_id=thread_id)
            else:
                pass

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "forum/post_list_delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "forum:post-list",
            kwargs={
                "category_id": self.kwargs["category_id"], ####це тре спіціально для роботи видалення
                "thread_id": self.kwargs["thread_id"],
            },
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs['category_id']
        context['thread_id'] = self.kwargs['thread_id']
        return context
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "forum/post_list_update.html"

    def get_success_url(self):
        return reverse_lazy(
            "forum:post-list",
            kwargs={
                "category_id":self.kwargs["category_id"],
                "thread_id":self.kwargs["thread_id"],
            }
        )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs['category_id']
        context['thread_id'] = self.kwargs['thread_id']
        return context
    



#     def reply(self, request, *args, **kwargs):
#         reply_form = ReplyPostForm(request.POST, request.FILES)
#         if reply_form.is_valid():
#             reply = reply_form.save(commit=False)
#             reply.author = request.user
#             reply.save()

#         else:
#             pass


#     def reply_post(self, request, *args, **kwargs):
#         reply_post_form = ReplyPostForm(request.POST, request.FILES)
#         if reply_post_form.is_valid():
#             reply = reply_post_form.save(commit = False)
#             reply.author = request.user
            
#             reply.save()
#             return redirect("")
#         else:
#             print("форма не валідна")


# class ReplyCreateView(LoginRequiredMixin,CreateView):
#     model = ReplyPost
#     form_class = ReplyPostForm
#     template_name = "forum/post_list.html"
#     context_object_name = "reply_posts"

#     def form_valid(self, form):
#         reply = form.save(commit=False)
#         reply.author = self.request.user
#         reply.save()
#         return redirect("")

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['reply_form'] = context['form']
#         context['reply_form'] = ReplyPostForm()
#         return context
    
#     def reply_post(self, request, *args, **kwargs):
#         reply_post_form = ReplyPostForm(request.POST, request.FILES)
#         if reply_post_form.is_valid():
#             reply = reply_post_form.save(commit = False)
#             reply.author = request.user
            
#             reply.save()
#             return redirect("")
#         else:
#             print("форма не валідна")


# class ReplyPostList(LoginRequiredMixin, ListView):
#     model = models.ReplyPost
#     context_object_name = "reply_posts"
#     template_name = "forum/post_list.html"
#     form_class = ReplyPostForm

#     # def get_context_data(self, **kwargs):

#     #     return context

#     # def get_queryset(self):
#     #     context = ReplyPost.object.filter(
            
#     #     )
