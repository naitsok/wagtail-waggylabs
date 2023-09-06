from django.utils.translation import gettext_lazy as _

from wagtail.blocks import StructBlock, ChoiceBlock

from waggylabs.blocks.styling import (
    TextStyleChoiceBlock, ListStyleChoiceBlock, ListItemStyleChoiceBlock
)
from waggylabs.blocks.wrapper import WrapperBlock


class PostSeriesItemBlock(StructBlock):
    """Item block to display contents for post series. E.g. main post
    and its subposts."""
    posts_style = ListStyleChoiceBlock(
        label=_('Post list style'),
    )
    post_style = ListItemStyleChoiceBlock(
        label=_('Post title item style'),
    )
    text_wrap = ChoiceBlock(
        required=False,
        choices=[
            ('', _('Text wrap')),
            ('text-nowrap', _('No text wrapping')),
        ],
        default='',
        label=_('Text wrapping'),
    )
    current_post_style = TextStyleChoiceBlock(
        required=True,
        choices=[
            ('active', _('Default')),
            ('fw-bold', _('Bold')),
            ('fw-bolder', _('Bolder')),
            ('fw-semibold', _('Semibold')),
            ('fw-normal', _('Normal')),
            ('fw-light', _('Light')),
            ('fw-lighter', _('Lighter')),
            ('fst-italic', _('Italic')),
            ('fw-bold fst-italic', _('Bold italic')),
            ('fw-bolder fst-italic', _('Bolder italic')),
            ('fw-semibold fst-italic', _('Semibold italic')),
            ('fw-light fst-italic', _('Light italic')),
            ('fw-lighter fst-italic', _('Lighter italic')),
            ('btn btn-primary', _('Button primary')),
            ('btn btn-secondary', _('Button secondary')),
            ('btn btn-success', _('Button success')),
            ('btn btn-danger', _('Button danger')),
            ('btn btn-warning', _('Button warning')),
            ('btn btn-info', _('Button info')),
            ('btn btn-outline-primary', _('Button outline primary')),
            ('btn btn-outline-secondary', _('Button outline secondary')),
            ('btn btn-outline-success', _('Button outline success')),
            ('btn btn-outline-danger', _('Button outline danger')),
            ('btn btn-outline-warning', _('Button outline warning')),
            ('btn btn-outline-info', _('Button outline info')),
        ],
        default='active',
        label=_('Current post style'),
    )
    

    class Meta:
        icon = 'post-series'
        label = _('Post series')
        form_template = 'waggylabs/blocks/form_template/post_series.html'
        template = 'waggylabs/blocks/template/post_series.html'


class PostSeriesBlock(WrapperBlock):
    """Block to display contents for post series. E.g. main post
    and its subposts."""
    item = PostSeriesItemBlock()
    
    class Meta:
        icon = 'post-series'
        label = _('Post series')
        help_text = _('If the post is included into a series, '
                      'its title appears in this block. The currenlty '
                      'shown post is highlihted according to the selected style.')