from django import forms
from django.utils.safestring import mark_safe
from markitup import settings
from markitup.widgets import MarkItUpWidget


class MultiMarkItUpWidget(MarkItUpWidget):
    def __init__(self, attrs=None,
                 markup_name='html'):
        self.markup_name = markup_name
        super(MarkItUpWidget, self).__init__(attrs)

    def _media(self):
        return forms.Media(
            css={'screen': (('techblog/markitup/css/all_sets.css'),)},
            js=(settings.JQUERY_URL,
                ('ext/markitup/ajax_csrf.js'),
                ('ext/markitup/jquery.markitup.js'),
                ('techblog/markitup/js/all_sets.js'))

        )
    media = property(_media)

    def render(self, name, value, attrs=None):
        html = super(MarkItUpWidget, self).render(name, value, attrs)

        html += ('<script type="text/javascript">'
                 '(function($) { '
                 '$(document).ready(function() {'
                 '  $("#%(id)s").markItUp(Markups.%(markup_name)s);'
                 '});'
                 '})(jQuery);'
                 '</script>') % {'id': attrs['id'], 'markup_name': self.markup_name}

        return mark_safe(html)
