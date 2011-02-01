from django import forms
from markitup.widgets import MarkItUpWidget
from techblog.models import Article

class ArticleForm(forms.ModelForm):
    #short = forms.TextField()
    #description = forms.TextField()
    class Meta(object):
        model = Article
        fields = ('title', 'short_raw', 'description_raw')
        widgets = {
            'short_raw': MarkItUpWidget(),
            'description_raw': MarkItUpWidget()
        }


