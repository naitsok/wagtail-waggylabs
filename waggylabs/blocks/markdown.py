from django import forms
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from wagtail.blocks import TextBlock

from wagtailmarkdown.blocks import render_markdown

from waggylabs.utils import pk_to_markdown
from waggylabs.widgets import MarkdownTextarea


class MarkdownBlock(TextBlock):
    """Replaces wagtail-markdown MarkdownBlock with this one in order to add LaTeX syntax highlighting
    and MathJax equations rendering during preview."""
    
    def __init__(self,
                 required=True,
                 help_text=_('Use this general text field to write paragraphs using Markdown syntax. '
                             'This markdown editor supports Emojis, LaTeX equation, referencing '
                             'figures, tables, equations, embeds, and listings. Emojies can be added '
                             'either directly with a Unicode code or using an alias that can be '
                             'found at https://www.webfx.com/tools/emoji-cheat-sheet/. '
                             'Inline and block equation can be added using standard LaTeX syntax, '
                             'references to equation are supproted using \\\u3164ref{...} or '
                             '\\\u3164eqref{...} syntax. Similarly \\\u3164ref{...} and '
                             '\\\u3164cite{...} commands are available to reference figures, '
                             'tables, blockquotes, listings, documents, as well as cite literature. '
                             'Note that final references and citing literature numbers will be '
                             'correctly generated on the published page, which can be previewed '
                             'before publishing Wagtail button at the bottom of the current web page. '
                             'The links to the pages of this website are added using the specific '
                             'syntax described at https://github.com/torchbox/wagtail-markdown#inline-links. '
                             'Finally use Ctrl+Space or Cmd+Space to invoke autocomplete for TeX commands '
                             '(starting from "\\" symbol) and for emojis (starting from ":" symbol).'),
                 rows=1,
                 max_length=None,
                 min_length=None,
                 validators=(),
                 min_height='300px', # e.g. 300px, valid CSS string
                 max_height='300px', # e.g. 500px, valid CSS string
                 stex_combine='true', # combine or not stex mode with markdown mode
                 # valid string that contains list of valid EasyMDE buttons + math patterns seprated by comma
                 # see the easymde-attach.js for availabe math patterns
                 toolbar=('bold,italic,strikethrough,heading,|,'
                                         'unordered-list,ordered-list,link,|,code,'
                                         'subscript,superscript,equation,matrix,'
                                         'align,|,preview,side-by-side,fullscreen,guide'),
                 # status bar: true for default status bar, false for no status bar, 
                 # string of comma-separated names for custom status bar
                 statusbar='true',
                 **kwargs):
        self.min_height = min_height
        self.max_height = max_height
        self.stex_combine = stex_combine
        self.toolbar = toolbar
        self.statusbar = statusbar
        super().__init__(required, help_text, rows, max_length, min_length, validators, **kwargs)
    
    @cached_property
    def field(self):
        field_kwargs = {
            'widget': MarkdownTextarea(
                attrs={'rows': self.rows },
                min_height=self.min_height,
                max_height=self.max_height,
                stex_combine=self.stex_combine,
                toolbar=self.toolbar,
                statusbar=self.statusbar
            )}
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)

    def render_basic(self, value, context):
        value = value.replace('\r', '')
        # replace all the encountered label with the label created by user 
        # plus page.pk, it is needed to avoid label conflicts when page
        # is rendered in a list, such as pagination or search results
        if 'page' in context:
            value = pk_to_markdown(value, context['page'].pk)
        return render_markdown(value, context)
    
    class Meta:
        icon = 'markdown'
        label_format = _('Text: {value}')
