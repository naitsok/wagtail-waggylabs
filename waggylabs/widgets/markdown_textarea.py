from django import forms
from django.conf import settings

from wagtail.telepath import register
from wagtail.widget_adapters import WidgetAdapter
from wagtail.utils.widgets import WidgetWithScript


class MarkdownTextarea(WidgetWithScript, forms.widgets.Textarea):
    """Replaces wagtail-markdown MarkdownTextarea with the one that is able to render MathJax."""
    def __init__(
        self,
        attrs={
            'rows': 1,
            'easymde-min-height': '100px', # e.g. 300px, valid CSS string
            'easymde-max-height': '100px', # e.g. 500px, valid CSS string
            'easymde-combine': 'true', # combine or not stex mode with markdown mode
            # valid string that contains list of valid EasyMDE buttons + math patterns
            # seprated by comma, see the easymde-attach.js for availabe math patterns
            'easymde-toolbar': ('bold,italic,strikethrough,heading,|,'
                                'unordered-list,ordered-list,link,|,code,'
                                'subscript,superscript,equation,matrix,'
                                'align,|,preview,side-by-side,fullscreen,guide'),
            # status bar: true for default status bar, false for no status bar,
            # string of comma-separated names for custom status bar
            'easymde-status': 'true',
        }
    ):
        super().__init__(attrs)

    def render_js_init(self, id_, name, value):
        """Attaches javascript init function to the widget."""
        return f'easymdeAttach("{id_}");'

    @property
    def media(self):
        """Adds static files nessary for work"""
        
        return forms.Media(
            css={
                "all": (
                    "https://cdn.jsdelivr.net/highlight.js/latest/styles/github.min.css", # for code highlighting
                    "waggylabs/vendor/codemirror/codemirror.min.css",
                    "waggylabs/vendor/codemirror/addon/hint/show-hint.css",
                    "waggylabs/vendor/easymde/easymde.min.css",
                    "waggylabs/css/widgets/easymde-darkmode.css",
                    "waggylabs/css/widgets/easymde-tweaks.css",
                    "waggylabs/css/widgets/easymde-highlight.css",
                )
            },
            js=(
                "https://cdn.jsdelivr.net/highlight.js/latest/highlight.min.js", # for code highlighting
                "waggylabs/vendor/marked/marked.min.js", # for custom markdown to avoid parsing LaTex equations
                "waggylabs/vendor/codemirror/codemirror.min.js", # For latex highlighting
                "waggylabs/vendor/codemirror/mode/stex/stex.js", # For latex highlighting
                "waggylabs/vendor/codemirror/addon/hint/show-hint.js", # For hints
                "waggylabs/vendor/easymde/easymde.min.js", # EasyMDE compiled with show-hint.js and stex.min.js
                "waggylabs/js/widgets/markdown-mathjax.js",
                "waggylabs/js/widgets/markdown-emoji.js",
                "waggylabs/js/widgets/markdown.js",
                "waggylabs/js/widgets/easymde-hint.js",
                "waggylabs/js/widgets/easymde-attach.js",
            ),
        )
        

class MathJaxMarkdownTextareaAdapter(WidgetAdapter):
    """Replaces the markdown-textarea MarkdownTextareaAdapter to have Javascript code from waggylabs"""
    js_constructor = "waggylabs.widgets.MarkdownTextarea"

    class Media:
        js = ["waggylabs/js/blocks/markdown-adapter.js"]


register(MathJaxMarkdownTextareaAdapter(), MarkdownTextarea)
