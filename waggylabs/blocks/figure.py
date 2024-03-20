from django.utils.translation import gettext_lazy as _

from wagtail.blocks import StructBlock
from wagtail.images.blocks import ImageChooserBlock

from waggylabs.blocks.markdown import MarkdownBlock
from waggylabs.blocks.label import LabelBlock


class FigureBlock(StructBlock):
    """Image with caption for StreamField."""
    image = ImageChooserBlock(
        required=True,
        label=_('Graphic'),
        )
    caption = MarkdownBlock(
        required=False,
        label=_('Figure caption'),
        help_text=None,
        min_height='100px',
        max_height='100px',
        stex_combine='true',
        toolbar=('bold,italic,strikethrough,|,unordered-list,'
                                'ordered-list,link,|,code,subscript,superscript,|,'
                                'preview,side-by-side,fullscreen,guide'),
        statusbar='false',
    )
    label = LabelBlock(
        max_length=50,
        required=False,
        form_classname='waggylabs-label-figure', # needed to render figure numbers
    )
    
    class Meta:
        template = 'waggylabs/blocks/template/figure.html'
        icon = 'image'
        label = _('Figure')
        label_format = _('Figure: {image}')