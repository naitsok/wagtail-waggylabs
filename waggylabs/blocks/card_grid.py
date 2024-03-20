from django.conf import settings
from django.utils.translation import gettext_lazy as _

from wagtail.blocks import (
    StructBlock, CharBlock, ListBlock,
    StreamBlock, ChoiceBlock
)
from wagtail.images.blocks import ImageChooserBlock


from waggylabs.blocks.links import (
    ExternalLinkBlock, InternalLinkBlock, IconEmailBlock,
    InfoTextBlock
)
from waggylabs.blocks.markdown import MarkdownBlock
from waggylabs.blocks.styling import CardStyleChoiceBlock, TextAlignmentChoiceBlock


class LinksBlock(StreamBlock):
    """Block to add different links."""
    external_link = ExternalLinkBlock()
    internal_link = InternalLinkBlock()
    email = IconEmailBlock()
    info_text = InfoTextBlock()
    
    class Meta:
        icon = 'link'
        label = _('Links for the card')

class CardBlock(StructBlock):
    """A one card block."""
    image = ImageChooserBlock(required=False, label=_('Image'))
    style = CardStyleChoiceBlock(required=False, label=_('Card style'))
    title = CharBlock(required=True, label=_('Card title'))
    subtitle = CharBlock(required=False, label=_('Card subtitle'))
    alignment = TextAlignmentChoiceBlock(required=False)
    text = MarkdownBlock(
        required=False,
        help_text=None,
        min_height='100px',
        max_height='100px',
        stex_combine='true',
        toolbar=('bold,italic,strikethrough,|,unordered-list,'
                                'ordered-list,link,|,code,subscript,superscript,|,'
                                'preview,side-by-side,fullscreen,guide'),
        statusbar='false',)
    links = LinksBlock(required=False)
    
    class Meta:
        icon = 'card-grid'
        label = _('Item of the card grid')
        template = 'waggylabs/blocks/template/card.html'
        form_template = 'waggylabs/blocks/form_template/card.html'
        label_format = _('Card: {title}')
        

CARD_GRID_COLUMNS = getattr(settings, 'WAGGYLABS_CARD_GRID_COLUMNS', 5)
class CardGridBlock(StructBlock):
    """Card grid block for StreamField."""
    height_style = ChoiceBlock(
        required=False,
        choices=[
            ('h-100', _('Equal height')),
            ('', _('Height wraps to content')),
        ],
        default='h-100',
        label=_('Card height style'),
    )
    grouping_style = ChoiceBlock(
        required=False,
        choices=[
            ('separate', _('Separate')),
            ('grouped', _('Grouped')),
        ],
        default='separate',
        label=_('Card grouping style'),
    )
    orientation_style = ChoiceBlock(
        required=False,
        choices=[
            ('vertical', _('Vertical')),
            ('horizontal', _('Horizontal')),
        ],
        default='vertical',
        label=_('Card orientation'),
    )
    columns = ChoiceBlock(
        required=False,
        choices=[
            (1, _('1 column')),
        ] + [
            (i + 1, str(i + 1) + _(' columns')) for i in
            range(1, CARD_GRID_COLUMNS)
        ],
        default=1,
        label=_('Number of columns'),
    )
    items = ListBlock(CardBlock())
    
    class Meta:
        icon = 'card-grid'
        label = _('Card grid')
        template = 'waggylabs/blocks/template/card_grid.html'
        form_template = 'waggylabs/blocks/form_template/card_grid.html'
        label_format = _('Card grid: {items}')
