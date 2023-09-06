from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from wagtail.blocks import StructBlock, ChoiceBlock

from waggylabs.blocks.markdown import MarkdownBlock
from waggylabs.blocks.wrapper import FooterWrapperBlock


class FooterMenuItemBlock(StructBlock):
    """Block item to add menu in the footer."""
    text_wrap = ChoiceBlock(
        required=False,
        choices=[
            ('', _('Text wrap')),
            ('text-nowrap', _('No text wrapping')),
        ],
        default='',
        label=_('Text wrapping'),
    )
    
    class Meta:
        icon = 'footer-menu'
        label = _('Footer main menu')
        template = 'waggylabs/blocks/template/footer_menu.html'


class FooterMenuBlock(FooterWrapperBlock):
    """Block to add menu in the footer."""
    item = FooterMenuItemBlock()
    
    class Meta:
        icon = 'footer-menu'
        label = _('Footer main menu')
        help_text = _('Adds the main menu without submenus to the footer.')