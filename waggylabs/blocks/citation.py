from django.utils.translation import gettext_lazy as _

from wagtail.blocks import CharBlock, StructBlock, URLBlock
from waggylabs.blocks.label import LabelBlock


class CitationBlock(StructBlock):
    """Block to add one citation with and refence it using LaTeX \cite{...} syntax."""
    citation = CharBlock(
        required=False,
        label=_('Title of the citation.'),
    )
    link = URLBlock(
        required=False,
        label=_('Citation link'),
    )
    label = LabelBlock(
        required=False,
        form_classname='waggylabs-label-cite',
        help_text=_('Cite literature using LaTeX \\cite{...} syntax in text markdown block.'),
    )
    
    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(local_blocks, **kwargs)
        self.child_blocks['citation'].field.widget.attrs.update({
            'placeholder': 'e.g. Author A, Author B, Title, Year, Journal.',
        })
        self.child_blocks['link'].field.widget.attrs.update({
            'placeholder': 'https://example.com',
        })
    
    class Meta:
        icon = 'citation'
        label = _('Citation')
        template = 'waggylabs/blocks/template/citation.html'
        form_template = 'waggylabs/blocks/form_template/citation.html'
        label_format = _('Cite: {citation}')