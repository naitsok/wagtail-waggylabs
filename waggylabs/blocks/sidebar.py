from django.utils.translation import gettext_lazy as _

from wagtail.blocks import StreamBlock, StructBlock, ChoiceBlock

from waggylabs.blocks.link_list import LinkListBlock
from waggylabs.blocks.page_info import PageInfoBlock
from waggylabs.blocks.post_archive import PostArchiveBlock
from waggylabs.blocks.post_category_list import PostCategoryListBlock
from waggylabs.blocks.post_highlights import PostHighlightsBlock
from waggylabs.blocks.post_series import PostSeriesBlock
from waggylabs.blocks.post_tag_list import PostTagListBlock
from waggylabs.blocks.sidebar_items import TextBlock, CitationsBlock, TableOfContentsBlock
from waggylabs.blocks.sidebar_tabs import SidebarTabsBlock
from waggylabs.blocks.visuals import VisualsBlock
        

class SidebarItemsBlock(StreamBlock):
    """Block that contains different sidebar items."""
    text = TextBlock()
    citations = CitationsBlock()
    link_list = LinkListBlock()
    page_info = PageInfoBlock()
    post_archive = PostArchiveBlock()
    post_category_list = PostCategoryListBlock()
    post_highlights = PostHighlightsBlock()
    post_series = PostSeriesBlock()
    post_tag_list = PostTagListBlock()
    tabs = SidebarTabsBlock()
    toc = TableOfContentsBlock()
    visuals = VisualsBlock()
    
    class Meta:
        icon = 'tasks'
        label = _('Items of the sidebar')
        block_counts = {
            'citations': { 'max_num': 1 },
            'tabs': { 'max_num': 1 },
            'toc': { 'max_num': 1 },
            'visuals': { 'max_num': 1 },
        }
        
        
class SidebarBlock(StructBlock):
    """Sidebar item block."""
    style = ChoiceBlock(
        required=False,
        choices=[
            ('', _('Fixed')),
            ('sticky-top', _('Sticky')),
        ],
        default='',
        label=_('Style of the sidebar'),
    )
    items = SidebarItemsBlock()
    
    class Meta:
        icon = 'sidebar'
        label = _('Sidebar')
        template = 'waggylabs/blocks/template/sidebar.html'