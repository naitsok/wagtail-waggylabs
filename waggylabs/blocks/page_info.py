
from django.utils.translation import gettext_lazy as _

from wagtail.blocks import (
    StructBlock, BooleanBlock, ChoiceBlock, CharBlock
)
from wagtail.users.models import UserProfile

from waggylabs.blocks.styling import (
    TextStyleChoiceBlock, TextAlignmentChoiceBlock
)
from waggylabs.blocks.wrapper import WrapperBlock


class PageInfoItemBlock(StructBlock):
    """Wrapper item to show page details such as author, creation
    date, etc. Rendered as a description list. Can be used in
    Sidebar."""
    show_user = BooleanBlock(
        required=False,
        label=_('Show the name of the page creator'),
    )
    user_header = CharBlock(
        required=False,
        label=_('Header of the page creator row'),
        help_text=_('Displays the header of the row '
                    'in which the page creator name is '
                    'displayed.'),
    )
    show_avatar = BooleanBlock(
        required=False,
        label=_('Show avatar'),
    )
    avatar_location = ChoiceBlock(
        required=False,
        choices=[
            ('start', _('Before username')),
            ('end', _('After username')),
        ],
        default='start',
        label=_('Avatar location'),
    )
    show_email = BooleanBlock(
        required=False,
        label=_('Show the email of page creator'),
    )
    email_header = CharBlock(
        required=False,
        label=_('Header of the page creator email row'),
        help_text=_('Displays the header of the row '
                    'in which the page creator email is '
                    'displayed.'),
    )
    show_first_published_at = BooleanBlock(
        required=False,
        label=_('Date of page publication'),
    )
    first_published_at_header = CharBlock(
        required=False,
        label=_('Header of the page publication date'),
        help_text=_('Displays the header of the row '
                    'in which the page publciation date is '
                    'displayed.'),
    )
    show_last_published_at = BooleanBlock(
        required=False,
        label=_('Date of last page update'),
    )
    last_published_at_header = CharBlock(
        required=False,
        label=_('Header of last page update'),
        help_text=_('Displays the header of the row '
                    'in which the last page update is '
                    'displayed.'),
    )
    datetime_style = ChoiceBlock(
        required=True,
        choices=[
            ('date', _('Only date')),
            ('datetime', _('Date and time')),
            ('timesince', _('Time since')),
        ],
        default='date',
        label=_('Date style'),
    )
    time_format = ChoiceBlock(
        required=True,
        choices=[
            ('G:i', _('24-hour format')),
            ('g:i A', _('12-hour format')),
        ],
        default='G:i',
        label=_('Time format'),
    )
    timesince_text = CharBlock(
        required=False,
        label=_('Time since text, e.g. ago'),
    )
    alignment = TextAlignmentChoiceBlock(
        label=_('Text alignment'),
    )
    row_header_style = TextStyleChoiceBlock(
        label=_('Row header style'),
    )
    row_data_style = TextStyleChoiceBlock(
        label=_('Row style'),
    )
    
    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(local_blocks, **kwargs)
        for block in self.child_blocks.values():
            if block.name != 'header':
                block.field.widget.attrs.update({
                    'placeholder': block.label,
                })
        
    def render(self, value, context):
        owner = context['page'].owner
        value['show_header'] = value['user_header'] or value['email_header'] or \
            value['first_published_at_header'] or value['last_published_at_header']
        value['dd_width'] = 'col-sm-9' if value['show_header'] else 'col-sm-12'
        if owner:
            value['username'] = owner.get_username()
            value['full_name'] = owner.get_full_name()
            value['email'] = owner.email
            value['avatar'] = UserProfile.get_for_user(owner).avatar
        value['first_published_at'] = context['page'].first_published_at
        value['last_published_at'] = context['page'].last_published_at
        return super().render(value, context)
    
    class Meta:
        icon = 'info'
        label = _('Page info')
        template = 'waggylabs/blocks/template/page_info.html'
        form_template = 'waggylabs/blocks/form_template/page_info.html'
    
    
class PageInfoBlock(WrapperBlock):
    """Block to show page info."""
    item = PageInfoItemBlock()
        
    class Meta:
        icon = 'info'
        label = _('Page info')
        help_text = _('Page info block displays the information about '
                      'page creator, created date, and last updated date.')
        