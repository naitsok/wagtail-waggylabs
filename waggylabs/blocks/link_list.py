from django.utils.translation import gettext_lazy as _

from django.apps import apps
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from wagtail.blocks import (
    ChoiceBlock, StructBlock, StreamBlock
)

from waggylabs.blocks.links import ExternalLinkBlock, InternalLinkBlock
from waggylabs.blocks.styling import ListStyleChoiceBlock

from waggylabs.blocks.wrapper import WrapperBlock, FooterWrapperBlock


class LinkListItemBlock(StructBlock):
    """Item block to list configurable links to external websites or internal pages."""
    link_list_style = ListStyleChoiceBlock(
        label=_('Link list style'),
    )
    link_style = ChoiceBlock(
        required=False,
        choices=[
            ('', 'Default list item'),
            ('list-group-item list-group-item-action', _('List group item')),
            ('list-group-item list-group-item-action list-group-item-primary', _('List group item primary')),
            ('list-group-item list-group-item-action list-group-item-secondary', _('List group item secondary')),
            ('list-group-item list-group-item-action list-group-item-success', _('List group item success')),
            ('list-group-item list-group-item-action list-group-item-danger', _('List group item danger')),
            ('list-group-item list-group-item-action list-group-item-warning', _('List group item warning')),
            ('list-group-item list-group-item-action list-group-item-info', _('List group item info')),
            ('list-group-item list-group-item-action list-group-item-light', _('List group item light')),
            ('list-group-item list-group-item-action list-group-item-dark', _('List group item dark')),
        ],
        default='',
        label=_('Link item style'),
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
    items = StreamBlock([
        ('external_link', ExternalLinkBlock()),
        ('internal_link', InternalLinkBlock()),
    ], use_json_field=True)
    
    class Meta:
        icon = 'link-list'
        label = _('List of links')
        template = 'waggylabs/blocks/template/link_list.html'
        form_template = 'waggylabs/blocks/form_template/link_list.html'
        
        
class LinkListBlock(WrapperBlock):
    """Block to list configurable links to external websites or internal pages."""
    item = LinkListItemBlock(label=_('List of links'))
    
    class Meta:
        icon = 'link-list'
        label = _('List of links')
        help_text = _('List of links shows list of custom link either to extrenal resource '
                      'or to any of the internal page.')
        
class FooterLinkListBlock(FooterWrapperBlock):
    """Block to list configurable links to external websites or internal pages in footer."""
    item = LinkListItemBlock(label=_('List of links'))
    
    class Meta:
        icon = 'link-list'
        label = _('List of links')
        help_text = _('List of links shows list of custom link either to extrenal resource '
                      'or to any of the internal page.')