from django.apps import apps
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from wagtail.blocks import (
    ChoiceBlock, StructBlock, PageChooserBlock,
    IntegerBlock, CharBlock
)

from waggylabs.blocks.styling import (
   ListStyleChoiceBlock, ListItemStyleChoiceBlock
)
from waggylabs.blocks.wrapper import WrapperBlock, FooterWrapperBlock


class PostArchiveItemBlock(StructBlock):
    """Item block to list the archive links to the posts published in the
    specified time interval."""
    post_list_page = PageChooserBlock(
        required=False,
        page_type='waggylabs.PostListPage',
        label=_('Root post list page'),
        help_text=_('Shows only posts that are descendant of this page. '
                    'If left empty, posts selected from all the posts are shown.'),
    )
    list_style = ListStyleChoiceBlock(
        label=_('Archive links list style'),
    )
    archives_number = IntegerBlock(
        required=True,
        min_value=0,
        default=0,
        label=_('Number of archive links to show'),
        help_text=_('If zero, all links are shown.')
    )
    list_item_style = ListItemStyleChoiceBlock(
        label=_('Archive link style'),
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
    archive_period = ChoiceBlock(
        required=True,
        choices=[
            ('day', _('By day')),
            ('month', _('By month')),
            ('year', _('By year')),
        ],
        default='month',
        label=_('Period of archive link'),
    )
    order_by = ChoiceBlock(
        required=True,
        choices=[
            ('DESC', _('Descneding')),
            ('ASC', _('Ascending'))
        ],
        default='DESC',
        label=_('Archive links order'),
    )
    more_archive_text = CharBlock(
        required=False,
        label=_('More archives button text'),
        help_text=_('When number of archive links is larger than '
                    'number of archive links to show, button to show '
                    'more links appears with the specified text.')
    )
        
    def render(self, value, context=None):
        post_page_model = apps.get_model('waggylabs', 'PostPage')
        archive_query = None
        more_archives_query = None
        
        if not value['post_list_page'] and \
            context['page'].specific_class.__name__ == 'PostListPage':
            value['post_list_page'] = context['page']
            
        if 'post_list_page' in value and value['post_list_page']:
            archive_query = post_page_model.objects.descendant_of(value['post_list_page'])\
                .live().dates('first_published_at', value['archive_period'], order=value['order_by'])
        
            if value['archives_number'] > 0 and archive_query.count() > value['archives_number']:
                archive_query = archive_query[0:value['archives_number']]
                more_archives_query = archive_query[value['archives_number']:]
            
        value['archives'] = archive_query
        value['more_archives'] = more_archives_query
        return super().render(value, context)
    
    class Meta:
        icon = 'archive'
        label = _('Post archives')
        template = 'waggylabs/blocks/template/post_archive.html'
        form_template = 'waggylabs/blocks/form_template/post_archive.html'
        
        
class PostArchiveBlock(WrapperBlock):
    """Block to list the archive links to the posts published in the
    specified time interval."""
    item = PostArchiveItemBlock()
    
    class Meta:
        icon = 'archive'
        label = _('Post archives')
        help_text = _('Post archives shows links to lists of posts that were published '
                      'during specified time periods.')
        
class FooterPostArchiveBlock(FooterWrapperBlock):
    """Block to list the archive links to the posts published in the
    specified time interval in footer."""
    item = PostArchiveItemBlock()
    
    class Meta:
        icon = 'archive'
        label = _('Post archives')
        help_text = _('Post archives shows links to lists of posts that were published '
                      'during specified time periods.')