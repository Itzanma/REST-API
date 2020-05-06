from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Article

@register(Article)
class ArticleIndex(AlgoliaIndex):
    fields = ('title', 'body', 'slug')
    settings = {'searchableAttributes': ['title', 'body', 'slug']}
    index_name = 'Article'