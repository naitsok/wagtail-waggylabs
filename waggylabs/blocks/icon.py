
from django.forms import CharField
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from wagtail.blocks import FieldBlock, ChoiceBlock

from waggylabs.widgets import IconInput


class IconBlock(FieldBlock):
    """Icon block with the IconInput widget."""
    def __init__(
        self,
        required=False,
        help_text=None,
        max_length=None,
        min_length=None,
        validators=(),
        label=_('Icon - start tying'),
        **kwargs,
    ):
        self.field_options = {
            "required": required,
            "help_text": help_text,
            "max_length": max_length,
            "min_length": min_length,
            "validators": validators,
        }
        self.label = label
        super().__init__(
            required=required,
            help_text=help_text,
            max_length=max_length,
            min_length=min_length,
            validators=validators,
            label=label,
            **kwargs)
    
    @cached_property
    def field(self):
        field_kwargs = { 
            'widget': IconInput(attrs={
                'placeholder': _('Icon - start typing')
            }), 
        }
        field_kwargs.update(self.field_options)
        return CharField(**field_kwargs)
    
    
class IconLocationBlock(ChoiceBlock):
    """Block to choose icon location."""
    def __init__(
        self,
        choices=[
            ('', _('Before text')),
            ('end', _('After text')),
        ],
        default='',
        label=_('Icon location'),
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