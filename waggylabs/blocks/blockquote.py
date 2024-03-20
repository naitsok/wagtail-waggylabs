from django.utils.translation import gettext_lazy as _

from wagtail.blocks import (
    CharBlock, StructBlock, ChoiceBlock, BooleanBlock
)

from waggylabs.widgets import DisabledOptionSelect

from waggylabs.blocks.label import LabelBlock
from waggylabs.blocks.markdown import MarkdownBlock
from waggylabs.blocks.styling import TextAlignmentChoiceBlock


class BlockQuoteBlock(StructBlock):
    """Quote block with text, author and source."""
    quote = MarkdownBlock(
        required=True,
        label=_('Quote text.'),
        help_text='',
        min_height='100px',
        max_height='100px',
        stex_combine='true',
        toolbar=('bold,italic,strikethrough,heading,|,unordered-list,'
                                'ordered-list,link,|,code,subscript,superscript,|,'
                                'preview,side-by-side,fullscreen,guide'),
        statusbar='false',
    )
    author = CharBlock(
        required=False,
        label=_('Author of the quoted text.')
    )
    source = CharBlock(
        required=False,
        label=_('Source of the quoted text.')
    )
    label = LabelBlock(
        max_length=50,
        required=False,
        form_classname='waggylabs-label-blockquote',
    )
    aligntment = TextAlignmentChoiceBlock(required=False)
    show_icon = BooleanBlock(
        required=False,
        label=_('Show quote icon'),
    )
    
    class Meta:
        icon = 'openquote'
        label = _('Blockquote')
        template = 'waggylabs/blocks/template/blockquote.html'
        label_format = _('Quote: {quote}')