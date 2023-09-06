from django import forms
from django.utils.functional import cached_property

from wagtail.core.blocks import TextBlock

from waggylabs.widgets import MathTextarea


class MathBlock(TextBlock):
    """A standalone math block with CodeMirror editor and MathJax math preview.
    Currently not in use."""
    
    def __init__(self,
                 required=True,
                 help_text=None,
                 rows=1,
                 max_length=None,
                 min_length=None,
                 validators=(),
                 mode="stex", # CodeMirror mode
                 **kwargs):
        self.mode = mode
        super().__init__(required, help_text, rows, max_length, min_length, validators, **kwargs)
        
    @cached_property
    def field(self):
        field_kwargs = {
            "widget": MathTextarea(attrs={
                "rows": self.rows,
                "codemirror-mode": self.mode,
                })
            }
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)

    def render_basic(self, value, context=None):
        value_lower = value.lower()
        if not (value_lower.startswith('\\begin') or  value_lower.startswith('$$')):
            value = '\\begin{equation}\n' + value + '\n\\end{equation}'
        return value
    
    class Meta:
        icon = 'superscript'
        label = 'Math'
