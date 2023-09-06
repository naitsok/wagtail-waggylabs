from django.utils.translation import gettext_lazy as _

from wagtail.blocks import (
    StructBlock, CharBlock,
    PageChooserBlock, URLBlock, EmailBlock
    )

from waggylabs.blocks.icon import IconBlock, IconLocationBlock
from waggylabs.blocks.styling import LinkStyleChoiceBlock


class ExternalLinkBlock(StructBlock):
    """Block to add links to external websites."""
    link = URLBlock(
        required=True,
        label=_('Link to external site'),
    )
    text = CharBlock(
        required=False,
        label=_('Text of the link'),
    )
    icon = IconBlock(
        label=_('Link icon'),
        required=False,
    )
    icon_location = IconLocationBlock(
        required=False,
        label=_('Link icon location')
    )
    style = LinkStyleChoiceBlock(
        required=False,
        label=_('Link style'),
    )
    
    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(local_blocks, **kwargs)
        self.child_blocks['link'].field.widget.attrs.update({
            'placeholder': 'example.com/username',
        })
        self.child_blocks['text'].field.widget.attrs.update({
            'placeholder': _('Text of the link'),
        })
    
    class Meta:
        icon = 'link-external'
        label = _('External link')
        form_template = 'waggylabs/blocks/form_template/external_link.html'
        template = 'waggylabs/blocks/template/external_link.html'
        label_format = _('External link')
    
    
class InternalLinkBlock(StructBlock):
    """Block to add links to this website."""
    link = PageChooserBlock(
        label=_('Link to a page of this site')
    )
    text = CharBlock(
        required=False,
        label=_('Text instead of page title'),
    )
    icon = IconBlock(
        label=_('Link icon'),
        required=False,
    )
    icon_location = IconLocationBlock(
        required=False,
        label=_('Link icon location'),
    )
    style = LinkStyleChoiceBlock(
        required=False,
        label=_('Link style'),
    )
    
    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(local_blocks, **kwargs)
        self.child_blocks['text'].field.widget.attrs.update({
            'placeholder': _('Text instead of page title'),
        })
    
    class Meta:
        icon = 'link'
        label = _('Internal link')
        form_template = 'waggylabs/blocks/form_template/internal_link.html'
        template = 'waggylabs/blocks/template/internal_link.html'
        label_format = _('Link: {link}')


class IconEmailBlock(StructBlock):
    """Block to add email with a possible icon."""
    email = EmailBlock(
        required=True,
        label=_('Email address'),
    )
    text = CharBlock(
        required=False,
        label=_('Text instead of email'),
    )
    icon = IconBlock(
        required=False,
        label=_('Email icon'),
    )
    icon_location = IconLocationBlock(
        required=False,
        label=_('Email icon location')
    )
    style = LinkStyleChoiceBlock(
        required=False,
        label=_('Email style'),
    )
    
    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(local_blocks, **kwargs)
        self.child_blocks['email'].field.widget.attrs.update({
            'placeholder': 'email@example.com',
        })
        self.child_blocks['text'].field.widget.attrs.update({
            'placeholder': _('Text to be displayed'),
        })
    
    class Meta:
        icon = 'mail'
        label = _('Email')
        form_template = 'waggylabs/blocks/form_template/email.html'
        template = 'waggylabs/blocks/template/email.html'
        label_format = _('Email: {email}')
        
        
class InfoTextBlock(StructBlock):
    """Block to add any type of text such as location or phone."""
    text = CharBlock(
        required=True,
        label=_('Phone, address, etc.'),
    )
    style = LinkStyleChoiceBlock(
        required=False,
        label=_('Style'),
    )
    icon = IconBlock(
        required=False,
        label=_('Icon'),
    )
    icon_location = IconLocationBlock(
        required=False,
        label=_('Icon location'),
    )
    
    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(local_blocks, **kwargs)
        self.child_blocks['text'].field.widget.attrs.update({
            'placeholder': _('Phone, address, etc.'),
        })
    
    class Meta:
        icon = 'info'
        label = _('Phone, address, etc.')
        form_template = 'waggylabs/blocks/form_template/info_text.html'
        template = 'waggylabs/blocks/template/info_text.html'
        label_format = _('Info: {text}')
        