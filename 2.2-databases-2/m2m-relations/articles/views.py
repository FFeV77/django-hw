from django.shortcuts import render
from django.db.models import Prefetch

from articles.models import Article, Tag, Scopes


def articles_list(request):
    template = 'articles/news.html'
    ordering = '-published_at'
    articles = Article.objects.order_by(ordering).prefetch_related('scopes__tag')
    context = {
        'object_list': articles,
    }

    return render(request, template, context)
