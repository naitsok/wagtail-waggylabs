from django.utils.translation import gettext_lazy as _

from wagtail.blocks import StructBlock, CharBlock, ChoiceBlock

from waggylabs.blocks.icon import IconBlock, IconLocationBlock
from waggylabs.blocks.styling import (
    CardStyleChoiceBlock, TextAlignmentChoiceBlock, HeaderStyleChoiceBlock
)


class BaseWrapperBlock(StructBlock):
    """base wrapper block for holding different blocks."""
    header = CharBlock(
        required=False,
        label=_('Header text'),
    )
    header_icon = IconBlock(
        required=False,
        label=_('Header icon'),
    )
    header_icon_location = IconLocationBlock(
        required=False,
        label=_('Header icon location'),
    )
    item = None
    
    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(local_blocks, **kwargs)
        if self.child_blocks['item'] is None:
            raise ValueError('Wrapper block cannot be used on its own. '
                             'It must be subclassed to provide non-None item '
                             'instance.')
        

class WrapperBlock(BaseWrapperBlock):
    """Wrapper block for sidebar blocks and body blocks with Bootstrap
    card style."""
    header_style = HeaderStyleChoiceBlock(
        required=False,
        label=_('Header style'),
    )
    block_style = CardStyleChoiceBlock()
    block_alignment = TextAlignmentChoiceBlock()
    
    class Meta:
        # icon and label must be defined in the subclass block
        form_template = 'waggylabs/blocks/form_template/wrapper.html'
        template = 'waggylabs/blocks/template/wrapper.html'
    
    
class FooterWrapperBlock(BaseWrapperBlock):
    """Wrapper block for rendering some of blocks in footer."""
    col_offset = ChoiceBlock(
        required=False,
        choices=[
            ('', _('No offset')),
            ('offset-lg-1', _('Narrow')),
            ('offset-lg-2', _('Medium')),
            ('offset-lg-3', _('Wide')),
        ],
        default='',
        label=_('Offset'),
    )
    col_width = ChoiceBlock(
        required=True,
        choices=[
            ('col-lg-2', _('Narrow')),
            ('col-lg-3', _('Medium')),
            ('col-lg-4', _('Wide')),
        ],
        default='col-lg-2',
        label=_('Width'),
    )
    
    class Meta:
        # icon and label must be defined in the subclass block
        form_template = 'waggylabs/blocks/form_template/footer_wrapper.html'
        template = 'waggylabs/blocks/template/footer_wrapper.html'