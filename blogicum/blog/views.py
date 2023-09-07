from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from blog.forms import CommentForm, PostForm, ProfileForm
from blog.mixins import PostChangeMixin, CommentChangeMixin
from blog.models import Category, Comment, Post, User
from blog.utils import get_query, make_paginator


def index(request):
    context = {'page_obj': make_paginator(get_query(Post.objects.all()),
                                          request)}
    return render(request, 'blog/index.html', context)


def category_posts(request, category_title):
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_title
    )

    context = {'category': category,
               'page_obj': make_paginator(get_query(category.posts.all()),
                                          request)}
    return render(request, 'blog/category.html', context)


def profile(request, username):
    profile = get_object_or_404(User, username=username)

    if username == request.user.username:
        posts = profile.posts.all().annotate(comment_count=Count('comments')
                                             ).order_by('-pub_date')
    else:
        posts = get_query(profile.posts.all())
    context = {'profile': profile,
               'page_obj': make_paginator(posts, request)}
    return render(request, 'blog/profile.html', context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'blog/user.html'

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user})

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.request.user)


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        q_object = (
            Q(id=self.kwargs['post_id']) & Q(author=self.request.user)
            | (
                Q(id=self.kwargs['post_id'])
                & Q(is_published=True)
                & Q(category__is_published=True)
                & Q(pub_date__lte=timezone.now())
            )
        )
        return get_object_or_404(Post, q_object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (self.get_object().comments.all()
                               .order_by('created_at'))
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:profile",
                       kwargs={"username": self.request.user})


class PostUpdateView(LoginRequiredMixin, PostChangeMixin, UpdateView):
    form_class = PostForm


class PostDeleteView(LoginRequiredMixin, PostChangeMixin, DeleteView):
    success_url = reverse_lazy('blog:index')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/detail.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post_detail",
                       kwargs={"post_id": self.kwargs['pk']})


class CommentUpdateView(LoginRequiredMixin, CommentChangeMixin, UpdateView):
    form_class = CommentForm


class CommentDeleteView(LoginRequiredMixin, CommentChangeMixin, DeleteView):
    pass
