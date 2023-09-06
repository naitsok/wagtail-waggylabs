from django.apps import apps
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from wagtail.blocks import (
    ChoiceBlock, StructBlock, PageChooserBlock,
    BooleanBlock, IntegerBlock
)

from waggylabs.blocks.styling import (
    ListStyleChoiceBlock, ListItemStyleChoiceBlock, BadgeStyleChoiceBlock,
    BadgeLocationChoiceBlock
)
from waggylabs.blocks.wrapper import WrapperBlock
from waggylabs.models.post_category import PostCategory, PostPagePostCategory


class PostCategoryListItemBlock(StructBlock):
    """Wrapper item to show post categories."""
    post_list_page = PageChooserBlock(
        required=False,
        page_type='waggylabs.PostListPage',
        label=_('Root post list page'),
        help_text=_('Shows post categories for the posts, which are '
                    'children of the selected post list page. '
                    'If left empty, the currently browsed post list page will '
                    'be used. Otherwise, no categories will be displayed.'),
    )
    categories_style = ListStyleChoiceBlock(
        label=_('Categories style'),
    )
    categories_number = IntegerBlock(
        required=True,
        default=10,
        min_value=0,
        label=_('Number of categories to show'),
        help_text=_('Depends on the selected order. '
                    'If equals to zero, then all categories are shown.'),
    )
    category_style = ListItemStyleChoiceBlock(
        label=_('Category item style'),
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
        default='created_at',
        label=_('Categories ordering'),
    )
    show_badges = BooleanBlock(
        required=False,
        label=_('Show number of posts per category'),
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
        category_query =  None
        
        if not value['post_list_page'] and \
            context['page'].specific_class.__name__ == 'PostListPage':
            value['post_list_page'] = context['page']
            
        if 'post_list_page' in value and value['post_list_page']:
            category_query = PostCategory.objects.filter(
                id__in=PostPagePostCategory.objects.filter(
                    post_page__in=post_page_model.objects.descendant_of(value['post_list_page']).live()
                ).values('post_category__id').distinct())

            if value['show_badges']:
                category_query = category_query.annotate(num_posts=Count('post_pages'))
        
            if not value['order_by']:
                value['order_by'] = '-created_at'
            category_query = category_query.order_by(value['order_by'])
            
            if value['categories_number'] > 0:
                category_query = category_query[0:value['categories_number']]
                
            
        value['categories'] = category_query
        return super().render(value, context)
        
    class Meta:
        icon = 'categories'
        label = _('Categories for posts')
        template = 'waggylabs/blocks/template/post_category_list.html'
        form_template = 'waggylabs/blocks/form_template/post_category_list.html'
        
        
class PostCategoryListBlock(WrapperBlock):
    """Block to show post categories."""
    item = PostCategoryListItemBlock()
    
    class Meta:
        icon = 'categories'
        label = _('Categories for posts')
        help_text = _('Post category list shows categories for posts that are childern of the specified post list page. '
                      'If post list page is not specified, the block must be located on a post list page.')