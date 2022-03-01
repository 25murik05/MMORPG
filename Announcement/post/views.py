from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView, FormView, View
from .models import *
from .form import *
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime, date, time
from django.urls import reverse
from .utils.permissions import IsAuthorMixin, NotIsAuthorMixin


class PostList(ListView):
    model = Post
    template_name = 'post/post.html'
    context_object_name = 'post'
    ordering = ['-id']
    paginate_by = 5


class PostDetail(DetailView):
    template_name = 'post/post_detail.html'
    queryset = Post.objects.all()


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'


def my_post(request):
    user = request.user
    if user.is_authenticated:
        contex = {
            'posts': Post.objects.filter(author=request.user).order_by('-id')
        }
        return render(request, 'my_post/myposts.html', contex)
    else:
        return render(request, 'my_post/come_in.html')


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'my_post/post_create.html'
    form_class = PostCreateForm
    success_url = '/my_posts/'

    def form_valid(self, form):
        post = form.save(commit=False)
        user = self.request.user
        post.author = user
        return super().form_valid(form)


class MyPostDetail(DetailView):
    template_name = 'my_post/my_post_detail.html'
    queryset = Post.objects.all()


class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'my_post/post_create.html'
    form_class = PostCreateForm
    success_url = '/my_posts/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def form_valid(self, form):
        post = form.save(commit=False)
        user = self.request.user
        post.author = user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'my_post/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/my_posts/'


class CommentsMyList(IsAuthorMixin, View):
    def get(self, request, *args, **kwargs):
        post_pk = kwargs['post_pk']
        post = Post.objects.get(pk=post_pk)
        qs = Comment.objects.order_by('datetime').filter(post=post)

        context = {
            'comments': qs,
            'post': post
        }
        return render(request, 'comment/comments_my_list.html', context)


class CommentsList(View):
    def get(self, request, *args, **kwargs):
        post_pk = kwargs['post_pk']
        post = Post.objects.get(pk=post_pk)
        qs = Comment.objects.order_by('datetime').filter(post=post)
        user = self.request.user

        context = {
            'comments': qs,
            'post': post,
            'user': user,
        }
        return render(request, 'comment/comments_list.html', context)


class CommentCreate(NotIsAuthorMixin, View):
    def get(self, request, **kwargs):
        form = CommentCreateForm(request.POST or None)
        post = Post.objects.get(pk=kwargs['post_pk'])

        context = {
            'form': form,
            'post': post
        }

        return render(request, 'comment/comment_create.html', context)

    def post(self, request, *args, **kwargs):
        form = CommentCreateForm(request.POST)
        user = request.user
        post_pk = kwargs['post_pk']

        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = user
            comment.post = Post.objects.get(pk=post_pk)
            comment.save()

        return redirect('post_list')


class CommentAccept(IsAuthorMixin, View):
    def get(self, request, *args, **kwargs):
        comment_pk = kwargs['comment_pk']

        comment = Comment.objects.get(pk=comment_pk)
        comment.approved = True
        comment.save()

        return redirect(request.META['HTTP_REFERER'])


class CommentReject(IsAuthorMixin, View):
    def get(self, request, *args, **kwargs):
        comment_pk = kwargs['comment_pk']

        comment = Comment.objects.get(pk=comment_pk)
        comment.approved = False
        comment.save()

        return redirect(request.META['HTTP_REFERER'])


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment/comment_delete.html'
    success_url = '/my_posts/'
    context_object_name = 'comment'

    def get_object(self, **kwargs ):
        comment_id = self.kwargs.get('comment_pk')
        comment = Comment.objects.get(pk=comment_id)
        return comment


