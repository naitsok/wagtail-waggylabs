from django.utils.translation import gettext_lazy as _

from wagtail.blocks import (
    StructBlock, ListBlock, ChoiceBlock, IntegerBlock
)
from wagtail.images.blocks import ImageChooserBlock

from waggylabs.widgets import DisabledOptionSelect

from waggylabs.blocks.markdown import MarkdownBlock
from waggylabs.blocks.styling import TextAlignmentChoiceBlock


class CarouselItem(StructBlock):
    """Block for the carousel item."""
    image = ImageChooserBlock(
        required=True,
        label=_('Picture for carousel'),
    )
    caption = MarkdownBlock(
        required=False,
        label=_('Text in front of the picture'),
        help_text='',
        min_height='100px',
        max_height='100px',
        stex_combine='true',
        toolbar=('bold,italic,strikethrough,heading,|,unordered-list,'
                                'ordered-list,link,|,code,subscript,superscript,|,'
                                'preview,side-by-side,fullscreen,guide'),
        statusbar='false',
    )
    interval = IntegerBlock(
        required=False,
        min_value=0,
        label=_('Interval in milliseconds to keep the item'),
        help_text=_('Enter the value in milliseconds to keep the current item '
                    'during this interval'),
        default=1000,
    )
    text_justify = TextAlignmentChoiceBlock(
        required=False,
        label=_('Text alignment'),
    )
    text_color = ChoiceBlock(
        required=False,
        choices=[
            ('text-light', _('Light')),
            ('text-dark', _('Dark')),
        ],
        default='text-light',
        label=_('Text color'),
    )
    text_size = ChoiceBlock(
        required=False,
        choices=[
            ('fs-6', _('Normal')),
            ('fs-5', _('Bigger')),
            ('fs-4', _('Big')),
            ('fs-3', _('Larger')),
            ('fs-2', _('Large')),
        ],
        default='fs-6',
        label=_('Text size'),
    )
    
    class Meta:
        icon = 'carousel'
        label = _('Item of the carousel')
        form_template = 'waggylabs/blocks/form_template/carousel_item.html'
        label_format = _('{image}')


class ImageCarouselBlock(StructBlock):
    """Carousel Block with images with possible caption."""
    switch = ChoiceBlock(
        required=True,
        choices=[
            ('carousel-fade', _('Fade after interval')),
            ('carousel', _('Change after interval')),
            ('false', _('Change on button')),
            ('false-fade', _('Fade on button')),
        ],
        default='carousel-fade',
        label=_('Carousel switch type'),
    )
    controls = ChoiceBlock(
        required=False,
        choices=[
            ('', _('No controls')),
            ('buttons', _('Left and right buttons')),
            ('indicators', _('Items indicators')),
            ('buttons_indicators', _('Buttons and indicators')),
        ],
        default='',
        label=_('Controls of the carousel'),
    )
    items = ListBlock(CarouselItem(), min_num=1)
        
    class Meta:
        icon = 'carousel'
        label = _('Picture Carousel')
        template = 'waggylabs/blocks/template/carousel.html'
        form_template = 'waggylabs/blocks/form_template/carousel.html'
        label_format = _('Carousel: {items}')