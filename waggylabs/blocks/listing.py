from django.utils.translation import gettext_lazy as _

from wagtail.blocks import StructBlock

from waggylabs.blocks.code import CodeBlock
from waggylabs.blocks.markdown import MarkdownBlock
from waggylabs.blocks.label import LabelBlock


class ListingBlock(StructBlock):
    """A code block with caption."""
    code = CodeBlock(label=None)
    caption = MarkdownBlock(
        required=False,
        label=_('Listing caption'),
        help_text=None,
        easymde_min_height='100px',
        easymde_max_height='100px',
        easymde_combine='true',
        easymde_toolbar_config=('bold,italic,strikethrough,|,unordered-list,'
                                'ordered-list,link,|,code,subscript,superscript,|,'
                                'preview,side-by-side,fullscreen,guide'),
        easymde_status='false',
    )
    label = LabelBlock(
        max_length=50,
        required=False,
        form_classname='waggylabs-label-listing', # needed to render references to listings
    )
    
    class Meta:
        icon = 'code'
        label = _('Listing')
        template = 'waggylabs/blocks/template/listing.html'
        form_template = 'waggylabs/blocks/form_template/listing.html'
        label_format = _('Listing: {code}')