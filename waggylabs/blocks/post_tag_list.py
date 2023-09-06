from django.apps import apps
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from wagtail.blocks import (
    ChoiceBlock, StructBlock, CharBlock, PageChooserBlock,
    BooleanBlock, IntegerBlock
)

from waggylabs.blocks.styling import (
    LinkStyleChoiceBlock, BadgeStyleChoiceBlock, BadgeLocationChoiceBlock
)
from waggylabs.blocks.wrapper import WrapperBlock
from waggylabs.models.post_tags import PostPageTag
# from waggylabs.models.post_page import PostPage


class PostTagListItemBlock(StructBlock):
    """Item block to show post tag."""
    post_list_page = PageChooserBlock(
        required=False,
        page_type='waggylabs.PostListPage',
        label=_('Root post list page'),
        help_text=_('Shows post tags for the posts, which are '
                    'children of the selected post list page. '
                    'If left empty, the currently browsed post list page will '
                    'be used. Otherwise, no categories will be displayed.'),
    )
    tags_style = LinkStyleChoiceBlock(
        required=False,
        label=_('Tags style'),
    )
    tags_number = IntegerBlock(
        required=True,
        default=10,
        min_value=0,
        label=_('Number of tags to show'),
        help_text=_('Depends on the selected order. '
                    'If equals to zero, then all tags are shown.')
    )
    order_by = ChoiceBlock(
        required=False,
        choices=[
            ('created_at', _('Older first')),
            ('-created_at', _('Newer first')),
            ('slug', _('By slug acsending')),
            ('-slug', _('By slug descending')),
            ('num_posts', _('By post number acsending')),
            ('-num_posts', _('By post number descending')),
        ],
        default='slug',
        label=_('Tags ordering'),
    )
    show_badges = BooleanBlock(
        required=False,
        label=_('Show number of posts per tag'),

    )
    badge_style = BadgeStyleChoiceBlock(
        label=_('Post number style'),
    )
    badge_location = BadgeLocationChoiceBlock(
        label=_('Post number location'),
    )
        
    def render(self, value, context):
        # needed to avoid circular imports
        post_page_model = apps.get_model('waggylabs', 'PostPage')
        tag_query =  None
        if not value['post_list_page'] and \
            context['page'].specific_class.__name__ == 'PostListPage':
            value['post_list_page'] = context['page']
            
        if 'post_list_page' in value and value['post_list_page']:
            tag_query = PostPageTag.objects.filter(
                content_object_id__in=post_page_model.objects.descendant_of(value['post_list_page']).live()
            ).values('tag__id', 'tag__slug', 'tag__name')

            if value['show_badges']:
                tag_query = tag_query.annotate(tag__num_posts=Count('tag__id'))
        
            if not value['order_by']:
                value['order_by'] = '-created_at'
            
            value['order_by'] = '-tag__' + value['order_by'][1:] if value['order_by'][0] == '-' else \
                'tag__' + value['order_by']
            tag_query = tag_query.order_by(value['order_by'])
                
            if value['tags_number'] > 0:
                tag_query = tag_query[0:value['tags_number']]
                
        value['tags'] = tag_query
        return super().render(value, context)
        
    class Meta:
        icon = 'tags'
        label = _('Tags for posts')
        template = 'waggylabs/blocks/template/post_tag_list.html'
        form_template = 'waggylabs/blocks/form_template/post_tag_list.html'
        
        
class PostTagListBlock(WrapperBlock):
    """Block to display tags for the posts under
    certain post list page."""
    
    item = PostTagListItemBlock()
    
    class Meta:
        icon = 'tags'
        label = _('Tags for posts')
        help_text = _('Tag list shows tags for posts that are childern of the specified post list page. '
                      'If post list page is not specified, post list page will be automatically selected '
                      'if block is located on a post list page or tags for all posts will be listed.')