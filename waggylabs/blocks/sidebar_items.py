from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from wagtail.blocks import StructBlock, ChoiceBlock

from waggylabs.blocks.markdown import MarkdownBlock
from waggylabs.blocks.wrapper import WrapperBlock


class TableOfContentsItemBlock(StructBlock):
    """Block to add table of contents in the sidebar."""
    text_wrap = ChoiceBlock(
        required=False,
        choices=[
            ('', _('Text wrap')),
            ('text-nowrap', _('No text wrapping')),
        ],
        default='',
        label=_('Text wrapping'),
    )
    
    def render_basic(self, value, context=None):
        return mark_safe(f'<div class="waggylabs-sidebar-toc {value["text_wrap"]}"></div>')

class TableOfContentsBlock(WrapperBlock):
    """Block to add table of contents in the sidebar."""
    item = TableOfContentsItemBlock()
    
    class Meta:
        icon = 'table-of-contents'
        label = _('Table of contents')
        help_text = _('Adds table of contents tab to the sidebar. All the '
                      'headers present on the text blocks of the page body '
                      'will appear as headers in the table of contents.')


class CitationsItemBlock(StructBlock):
    """Adds block with references to the side bar. Only one such block can be
    added."""
    text_wrap = ChoiceBlock(
        required=False,
        choices=[
            ('', _('Text wrap')),
            ('text-nowrap', _('No text wrapping')),
        ],
        default='',
        label=_('Text wrapping'),
    )
    
    def render_basic(self, value, context=None):
        return mark_safe(f'<div class="waggylabs-sidebar-literature {value["text_wrap"]}"></div>')
    
    class Meta:
        icon = 'citation'
        label = _('References')
        

class CitationsBlock(WrapperBlock):
    """Adds block with references to the side bar. Only one such block can be
    added."""
    item = CitationsItemBlock()
    
    class Meta:
        icon = 'citation'
        label = _('References')
        help_text = _('Adds references to the sidebar.')
        
        
class TextBlock(WrapperBlock):
    """Block to add a simple text piece in the sidebar."""
    item = MarkdownBlock(
        required=True,
        label=_('Text'),
        help_text=None,
        min_height='100px',
        max_height='100px',
        stex_combine='true',
        toolbar=('bold,italic,strikethrough,|,unordered-list,'
                                'ordered-list,link,|,code,subscript,superscript,|,'
                                'preview,side-by-side,fullscreen,guide'),
        statusbar='false',
    )
    
    class Meta:
        icon = 'markdown'
        label = _('Sidebar text')
        help_text = _('Adds text block the sidebar.')
        