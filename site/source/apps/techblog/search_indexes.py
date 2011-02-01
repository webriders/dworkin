from haystack.indexes import RealTimeSearchIndex, CharField, DateTimeField
from haystack import site
from models import Article

class ArticleIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    author = CharField(model_attr='author')
    date = DateTimeField(model_attr='date')

site.register(Article, ArticleIndex)
