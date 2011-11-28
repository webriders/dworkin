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


#
# http://djangosnippets.org/snippets/2453/
#
# HTML allows an option in a <select> to be disabled. In other words it will appear
# in the list of choices but won't be selectable. This is done by adding a 'disabled'
# attribute to the <option> tag, for example: <option value="" disabled="disabled">Disabled option</option>
#
# This code subclasses the regular Django Select widget, overriding
# the render_option method to allow disabling options.
#
# Example of usage:
#
# class FruitForm(forms.Form):
#    choices = (('apples', 'Apples'),
#               ('oranges', 'Oranges'),
#               ('bananas', {'label': 'Bananas',
#                            'disabled': True}),    # Yes, we have no bananas
#               ('grobblefruit', 'Grobblefruit'))
#
#    fruit = forms.ChoiceField(choices=choices, widget=SelectWithDisabled())

from django.forms.widgets import Select
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape


class SelectWithDisabled(Select):
    """
    Subclass of Django's select widget that allows disabling options.
    To disable an option, pass a dict instead of a string for its label,
    of the form: {'label': 'option label', 'disabled': True}
    """
    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_unicode(option_value)
        if (option_value in selected_choices):
            selected_html = u' selected="selected"'
        else:
            selected_html = ''
        disabled_html = ''
        if isinstance(option_label, dict):
            if dict.get(option_label, 'disabled'):
                disabled_html = u' disabled="disabled"'
            option_label = option_label['label']
        return u'<option value="%s"%s%s>%s</option>' % (
            escape(option_value), selected_html, disabled_html,
            conditional_escape(force_unicode(option_label)))
