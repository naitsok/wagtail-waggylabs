from django.apps import apps
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from wagtail.blocks import (
    ChoiceBlock, StructBlock, PageChooserBlock,
    IntegerBlock
)

from waggylabs.blocks.styling import (
   ListStyleChoiceBlock, ListItemStyleChoiceBlock
)
from waggylabs.blocks.wrapper import WrapperBlock, FooterWrapperBlock


class PostHighlightsItemBlock(StructBlock):
    """Item block to list the selected number of posts based on the
    post list page."""
    post_list_page = PageChooserBlock(
        required=False,
        page_type='waggylabs.PostListPage',
        label=_('Root post list page'),
        help_text=_('Shows only posts that are descendant of this page. '
                    'If left empty, posts selected from all the posts are shown.'),
    )
    posts_style = ListStyleChoiceBlock(
        label=_('Post list style'),
    )
    posts_number = IntegerBlock(
        required=True,
        min_value=0,
        label=_('Number of posts to show'),
        help_text=_('If zero, all post are shown.')
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
    order_by = ChoiceBlock(
        required=False,
        choices=[
            ('created_at', _('Older first')),
            ('-created_at', _('Newer first')),
            ('title', _('By title acsending')),
            ('-title', _('By title descending')),
            ('owner__username', _('By author ascending')),
            ('-owner__username', _('By author descending')),
        ],
        default='-created_at',
        label=_('Posts ordering'),
    )
        
    def render(self, value, context=None):
        post_page_model = apps.get_model('waggylabs', 'PostPage')
        post_query = None
        if 'post_page_list' in value and value['post_page_list']:
            post_query = post_page_model.objects.descendant_of(value['post_list_page']).live()
        else:
            post_query = post_page_model.objects.live()
            
        post_query = post_query.order_by(value['order_by'])
        
        if value['posts_number'] > 0:
            post_query = post_query[0:value['posts_number']]
            
        value['posts'] = post_query
        return super().render(value, context)
    
    class Meta:
        icon = 'light-bulb'
        label = _('Post highlights')
        template = 'waggylabs/blocks/template/post_highlights.html'
        form_template = 'waggylabs/blocks/form_template/post_highlights.html'
        
        
class PostHighlightsBlock(WrapperBlock):
    """Block to list the selected number of posts based on the
    post list page."""
    item = PostHighlightsItemBlock()
    
    class Meta:
        icon = 'light-bulb'
        label = _('Post highlights')
        help_text = _('Post highlights shows list of post titles sorted according the selected ordering. '
                      'Block can be used, for example to display list of latest blog post '
                      'titles or news.')
        
class FooterPostHighlightsBlock(FooterWrapperBlock):
    """Block to list the selected number of posts based on the
    post list page in footer."""
    item = PostHighlightsItemBlock()
    
    class Meta:
        icon = 'light-bulb'
        label = _('Post highlights')
        help_text = _('Post highlights shows list of post titles sorted according the selected ordering. '
                      'Block can be used, for example to display list of latest blog post '
                      'titles or news.')