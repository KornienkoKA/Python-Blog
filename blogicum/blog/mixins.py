from django.shortcuts import redirect
from django.urls import reverse_lazy

from blog.models import Comment, Post


class PostChangeMixin:
    model = Post
    template_name = 'blog/create.html'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author == request.user:
            return super().dispatch(request, *args, **kwargs)
        return redirect('blog:post_detail', post_id=kwargs['pk'])


class CommentChangeMixin:
    model = Comment
    template_name = 'blog/comment.html'

    pk_url_kwarg = "comment_id"

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author == request.user:
            return super().dispatch(request, *args, **kwargs)
        return redirect('blog:post_detail', post_id=kwargs['post_id'])

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'post_id': self.kwargs['post_id']})
