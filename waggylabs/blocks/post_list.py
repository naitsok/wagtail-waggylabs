from django.utils.translation import gettext_lazy as _

from wagtail.blocks import (
    CharBlock, ChoiceBlock, StructBlock, IntegerBlock,
    BooleanBlock
)

from waggylabs.blocks.icon import IconBlock, IconLocationBlock
from waggylabs.blocks.styling import (
    HeaderStyleChoiceBlock, CardStyleChoiceBlock
) 
from waggylabs.models.post_page import PostPage
from waggylabs.widgets import DisabledOptionSelect


class PostListBlock(StructBlock):
    """Block to show posts and their pagination."""
    show_pinned_posts = BooleanBlock(
        required=False,
        label=_('Show pinned posts'),
    )
    pinned_posts_header = CharBlock(
        required=False,
        label=_('Pinned posts header'),
    )
    pinned_posts_icon = IconBlock(
        required=False,
        label=_('Pinned posts icon'),
    )
    pinned_posts_icon_location = IconLocationBlock(
        required=False,
        label=_('Pinned posts icon location'),
    )
    pinned_posts_header_style = HeaderStyleChoiceBlock(
        required=False,
        label=_('Pinned posts header style'),
    )
    posts_header = CharBlock(
        required=False,
        label=_('Post list header'),
    )
    posts_icon = IconBlock(
        required=False,
        label=_('Post list icon'),
    )
    posts_icon_location = IconLocationBlock(
        required=False,
        label=_('Post list icon location'),
    )
    posts_header_style = HeaderStyleChoiceBlock(
        required=False,
        label=_('Post list header style'),
    )
    first_page_text = CharBlock(
        required=False,
        label=_('First page button text'),
    )
    first_page_icon = IconBlock(
        required=False,
        label=_('First page button icon'),
    )
    previous_page_text = CharBlock(
        required=False,
        label=_('Previous page button text'),
    )
    previous_page_icon = IconBlock(
        required=False,
        label=_('Previous page button icon'),
    )
    next_page_text = CharBlock(
        required=False,
        label=_('Next page button text'),
    )
    next_page_icon = IconBlock(
        required=False,
        label=_('Next page button icon'),
    )
    last_page_text = CharBlock(
        required=False,
        label=_('Last page button text'),
    )
    last_page_icon = IconBlock(
        required=False,
        label=_('Last page button icon'),
    )
    post_style = CardStyleChoiceBlock(
        required=False,
        label=_('Post style in the list'),
    )
    post_title_style = HeaderStyleChoiceBlock(
        required=False,
        label=_('Post title style'),
    )
    page_alignment = ChoiceBlock(
        required=True,
        choices=[
            ('justify-content-start', _('Left')),
            ('justify-content-center', _('Center')),
            ('justify-content-end', _('Right')),
        ],
        default='justify-content-center',
        label=_('Paginator alignment'),
    )
    page_size = ChoiceBlock(
        required=False,
        choices=[
            ('', _('Normal')),
            ('pagination-sm', _('Small')),
            ('pagination-lg', _('Large')),
        ],
        default='',
        label=_('Paginator text size'),
    )
    posts_per_page = IntegerBlock(
        required=True,
        min_value=1,
        label=_('Posts per page'),
    )
    order_by = ChoiceBlock(
        required=True,
        choices=[
            ('created_at', _('Older first')),
            ('-created_at', _('Newer first')),
            ('slug', _('By slug acsending')),
            ('-slug', _('By slug descending')),
        ],
        default='-created_at',
        label=_('Categories ordering'),
    )
    show_scrollspy = BooleanBlock(
        required=False,
        label=_('Highlight post categories and tags when '
                'corresponding sidebar blocks are present')
    )
    show_username = BooleanBlock(
        required=False,
        label=_('Show username'),
    )
    show_avatar = BooleanBlock(
        required=False,
        label=_('Show avatar'),
    )
    show_first_published_at = BooleanBlock(
        required=False,
        label=_('Date of page publication'),
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
    show_time = BooleanBlock(
        required=False,
        label=_('Show time in the date fields'),
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
    
    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(local_blocks, **kwargs)
        for block in self.child_blocks.values():
            block.field.widget.attrs.update({
                'placeholder': block.label,
            })
            
    def render(self, value, context):
        page = context['page']
        
        pinned_posts_query = PostPage.objects.descendant_of(page).live() \
            .select_related('owner__wagtail_userprofile').filter(pin_in_list=True)
        posts_query = PostPage.objects.descendant_of(page).live() \
                .select_related('owner__wagtail_userprofile')
        if value['show_scrollspy']:
            posts_query = posts_query.prefetch_related('post_categories', 'tags')
        if value['show_pinned_posts']:
            posts_query = posts_query.filter(pin_in_list=False)
            
        if not value['order_by']:
            value['order_by'] = '-created_at'
            
        pinned_posts_query = pinned_posts_query.order_by(value['order_by'])
        posts_query = posts_query.order_by(value['order_by'])
            
        value['pinned_posts'] = pinned_posts_query
        value['posts'] = posts_query
        value['show_footer'] = value['show_username'] or value['show_avatar'] or \
            value['show_first_published_at'] or value['show_time']
        return super().render(value, context)
    
    class Meta:
        icon = 'post-list-page'
        label = _('Post list')
        template = 'waggylabs/blocks/template/post_list.html'
        form_template = 'waggylabs/blocks/form_template/post_list.html'
        help_text = _('Post list block controls the appearence list of posts '
                      'on the page. It can include pinned posts that always appear '
                      'on the first page of page list. Number of post per page, '
                      'their appearance in the list, paginator styles can be alo set.')
    