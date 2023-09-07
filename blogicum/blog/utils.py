from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone


POSTS_ON_PAGE = 10


def make_paginator(posts, request):
    paginator = Paginator(posts, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def get_query(param):
    return param.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    ).annotate(comment_count=Count('comments')).order_by('-pub_date')
