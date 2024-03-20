from django.utils.translation import gettext_lazy as _

from wagtail.blocks import StructBlock
from wagtail.embeds.blocks import EmbedBlock as WagtailEmbedBlock

from waggylabs.blocks.label import LabelBlock
from waggylabs.blocks.markdown import MarkdownBlock


class EmbedBlock(StructBlock):
    """An embed block with caption and label."""
    embed = WagtailEmbedBlock(
        label=_('URL of embedding')
    )
    caption = MarkdownBlock(
        required=False,
        label=_('Embed caption'),
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
        form_classname='waggylabs-label-embed', # needed to render embed numbers
    )
    
    class Meta:
        icon = 'embed'
        template = 'waggylabs/blocks/template/embed.html'
        label = _('Embed')
        label_format = _('Embed: {embed}')