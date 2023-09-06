from django.utils.translation import gettext_lazy as _

from wagtail.blocks import ChoiceBlock


class LinkStyleChoiceBlock(ChoiceBlock):
    """Block to choose link style (button or link) from 
    Bootstrap styles."""
    def __init__(
        self,
        choices=[
            ('', _('Default')),
            
            ('card-link', _('Card link')),
            ('nav-link', _('Navigation bar link')),
            ('nav-link active', _('Navigation bar active link')),
            ('link-primary', _('Primary link')),
            ('link-secondary', _('Secondary link')),
            ('link-success', _('Success link')),
            ('link-danger', _('Danger link')),
            ('link-warning', _('Warning link')),
            ('link-info', _('Info link')),
            ('link-light', _('Light link')),
            ('link-dark', _('Dark link')),
            ('nav-link link-primary', _('Primary link, no underline')),
            ('nav-link link-secondary', _('Secondary link, no underline')),
            ('nav-link link-success', _('Success link, no underline')),
            ('nav-link link-danger', _('Danger link, no underline')),
            ('nav-link link-warning', _('Warning link, no underline')),
            ('nav-link link-info', _('Info link, no underline')),
            ('nav-link link-light', _('Light link, no underline')),
            ('nav-link link-dark', _('Dark link, no underline')),
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
        default='',
        label=_('Link style'),
        required=False,
        help_text=None,
        validators=(),
        **kwargs):
        super().__init__(
            choices,
            default,
            required,
            help_text,
            validators,
            label=label,
            **kwargs)
        
        
class TextStyleChoiceBlock(ChoiceBlock):
    """Block to choose style for text for different blocks."""
    def __init__(
        self,
        choices=[
            ('', _('Default')),
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
        default='',
        label=_('Text style'),
        required=False,
        help_text=None,
        validators=(),
        **kwargs):
        super().__init__(
            choices,
            default,
            required,
            help_text,
            validators,
            label=label,
            **kwargs)
        
        
class CardStyleChoiceBlock(ChoiceBlock):
    """Block to choose style of Bootstrap card."""
    def __init__(
        self,
        choices=[
            ('', _('Default')),
            ('text-bg-primary', _('Primary')),
            ('text-bg-secondary', _('Secondary')),
            ('text-bg-success', _('Success')),
            ('text-bg-danger', _('Danger')),
            ('text-bg-warning', _('Warning')),
            ('text-bg-info', _('Info')),
            ('text-bg-light', _('Light')),
            ('text-bg-dark', _('Dark')),
            ('border-primary', _('Border primary')),
            ('border-secondary', _('Border secondary')),
            ('border-success', _('Border success')),
            ('border-danger', _('Border danger')),
            ('border-warning', _('Border warning')),
            ('border-info', _('Border info')),
            ('border-light', _('Border light')),
            ('border-dark', _('Border dark')),
            ('border-0', _('No border')),
            ('border-0 mp-0', _('No border, no margin')),
        ],
        default='',
        label=_('Card style'),
        required=False,
        help_text=None,
        validators=(),
        **kwargs):
        super().__init__(
            choices,
            default,
            required,
            help_text,
            validators,
            label=label,
            **kwargs)
        
        
class TextAlignmentChoiceBlock(ChoiceBlock):
    """Block for text alignment."""
    def __init__(
        self,
        choices=[
            ('', _('Left')),
            ('text-center', _('Center')),
            ('text-end', _('Right')),
        ],
        default='',
        label=_('Text alignment'),
        required=False,
        help_text=None,
        validators=(),
        **kwargs):
        super().__init__(
            choices,
            default,
            required,
            help_text,
            validators,
            label=label,
            **kwargs)
        
        
class HeaderStyleChoiceBlock(ChoiceBlock):
    """Block for header style."""
    def __init__(
        self,
        choices=[
            ('', _('Default')),
            ('h1', _('Header 1')),
            ('h2', _('Header 2')),
            ('h3', _('Header 3')),
            ('h4', _('Header 4')),
            ('h5', _('Header 5')),
            ('h6', _('Header 6')),
            ('display-1', _('Display header 1')),
            ('display-2', _('Display header 2')),
            ('display-3', _('Display header 3')),
            ('display-4', _('Display header 4')),
            ('display-5', _('Display header 5')),
            ('display-6', _('Display header 6')),
            ('fw-bold', 'Bold'),
            ('fw-bolder', 'Bolder'),
            ('fw-semibold', 'Semibold'),
            ('fw-normal', 'Normal'),
            ('fw-light', 'Light'),
            ('fw-lighter', 'Lighter'),
            ('fst-italic', 'Italic'),
            ('fw-bold fst-italic', 'Bold italic'),
            ('fw-bolder fst-italic', 'Bolder italic'),
            ('fw-semibold fst-italic', 'Semibold italic'),
            ('fw-light fst-italic', 'Light italic'),
            ('fw-lighter fst-italic', 'Lighter italic'),
        ],
        default='',
        label=_('Header style'),
        required=False,
        help_text=None,
        validators=(),
        **kwargs):
        super().__init__(
            choices,
            default,
            required,
            help_text,
            validators,
            label=label,
            **kwargs)
        
        
class ListStyleChoiceBlock(ChoiceBlock):
    """Block for list style."""
    def __init__(
        self,
        choices=[
            ('', _('Default list')),
            ('list-unstyled', _('Unstyled list')),
            ('list-numbered', _('Numbered list')),
            ('list-group', _('List group')),
            ('list-group list-group-flush', _('List group, no outer borders')),
            ('list-group list-group-numbered', _('Numbered list group')),
            ('list-group list-group-numbered list-group-flush', _('Numbered list group, no outer borders')),
        ],
        default='',
        label=_('List style'),
        required=False,
        help_text=None,
        validators=(),
        **kwargs):
        super().__init__(
            choices,
            default,
            required,
            help_text,
            validators,
            label=label,
            **kwargs)
        
        
class ListItemStyleChoiceBlock(ChoiceBlock):
    """Block for list item style."""
    def __init__(
        self,
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
            ('card-link', _('Card link')),
            ('nav-link', _('Navigation bar link')),
            ('nav-link active', _('Navigation bar active link')),
            ('link-primary', _('Primary link')),
            ('link-secondary', _('Secondary link')),
            ('link-success', _('Success link')),
            ('link-danger', _('Danger link')),
            ('link-warning', _('Warning link')),
            ('link-info', _('Info link')),
            ('link-light', _('Light link')),
            ('link-dark', _('Dark link')),
            ('nav-link link-primary', _('Primary link, no underline')),
            ('nav-link link-secondary', _('Secondary link, no underline')),
            ('nav-link link-success', _('Success link, no underline')),
            ('nav-link link-danger', _('Danger link, no underline')),
            ('nav-link link-warning', _('Warning link, no underline')),
            ('nav-link link-info', _('Info link, no underline')),
            ('nav-link link-light', _('Light link, no underline')),
            ('nav-link link-dark', _('Dark link, no underline')),
        ],
        default='',
        label=_('List item style'),
        required=False,
        help_text=None,
        validators=(),
        **kwargs):
        super().__init__(
            choices,
            default,
            required,
            help_text,
            validators,
            label=label,
            **kwargs)
        
        
class BadgeStyleChoiceBlock(ChoiceBlock):
    """Block for list style."""
    def __init__(
        self,
        choices=[
            ('text-bg-primary', _('Primary')),
            ('text-bg-secondary', _('Secondary')),
            ('text-bg-success', _('Success')),
            ('text-bg-danger', _('Danger')),
            ('text-bg-warning', _('Warning')),
            ('text-bg-info', _('Info')),
            ('text-bg-light', _('Light')),
            ('text-bg-dark', _('Dark')),
            ('rounded-pill text-bg-primary', _('Rounded primary')),
            ('rounded-pill text-bg-secondary', _('Rounded secondary')),
            ('rounded-pill text-bg-success', _('Rounded success')),
            ('rounded-pill text-bg-danger', _('Rounded danger')),
            ('rounded-pill text-bg-warning', _('Rounded warning')),
            ('rounded-pill text-bg-info', _('Rounded info')),
            ('rounded-pill text-bg-light', _('Rounded light')),
            ('rounded-pill text-bg-dark', _('Rounded dark')),
        ],
        default='text-bg-primary',
        label=_('Badge style'),
        required=False,
        help_text=None,
        validators=(),
        **kwargs):
        super().__init__(
            choices,
            default,
            required,
            help_text,
            validators,
            label=label,
            **kwargs)
        

class BadgeLocationChoiceBlock(ChoiceBlock):
    """Block for list style."""
    def __init__(
        self,
        choices=[
            ('', _('Default')),
            ('position-absolute top-0 start-100 translate-middle', _('Top right corner')),
            ('position-absolute top-0 start-0 translate-middle', _('Top left corner')),
            ('position-absolute top-100 start-100 translate-middle', _('Bottom right corner')),
            ('position-absolute top-100 start-0 translate-middle', _('Bottom left corner')),
        ],
        default='',
        label=_('Badge location'),
        required=False,
        help_text=None,
        validators=(),
        **kwargs):
        super().__init__(
            choices,
            default,
            required,
            help_text,
            validators,
            label=label,
            **kwargs)