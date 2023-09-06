
from django.utils.translation import gettext_lazy as _

from wagtail.blocks import StructBlock, ChoiceBlock, StreamBlock

from waggylabs.blocks.link_list import LinkListBlock
from waggylabs.blocks.page_info import PageInfoBlock
from waggylabs.blocks.post_archive import PostArchiveBlock
from waggylabs.blocks.post_category_list import PostCategoryListBlock
from waggylabs.blocks.post_highlights import PostHighlightsBlock
from waggylabs.blocks.post_series import PostSeriesBlock
from waggylabs.blocks.post_tag_list import PostTagListBlock
from waggylabs.blocks.sidebar_items import TextBlock, CitationsBlock, TableOfContentsBlock
from waggylabs.blocks.styling import LinkStyleChoiceBlock
from waggylabs.blocks.visuals import VisualsBlock
from waggylabs.blocks.wrapper import WrapperBlock


class TabItemsBlock(StreamBlock):
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
    toc = TableOfContentsBlock()
    visuals = VisualsBlock()
    
    class Meta:
        icon = 'tasks'
        label = _('Item of the sidebar')
        block_counts = {
            'citations': { 'max_num': 1 },
            'toc': { 'max_num': 1 },
            'visuals': { 'max_num': 1 },
        }

        
class SidebarTabsItemBlock(StructBlock):
    """Sidebar iten block with tabs for the the page. Tabs can contain
    contents (generated from headers on page), page visuals."""
    tabs_style = ChoiceBlock(
        required=False,
        choices=[
            ('nav nav-tabs', _('Tabs')),
            ('nav nav-pills', _('Pills')),
            ('nav nav-pills nav-fill', _('Wide pills')),
        ],
        default='nav nav-tabs',
        label=_('Tabs style'),
    )
    buttons_style = LinkStyleChoiceBlock(
        required=False,
        label=_('Tab buttons style'),
    )
    tabs_font_size = ChoiceBlock(
        required=False,
        choices=[
            ('', _('Default')),
            ('fs-6', _('Normal')),
            ('fs-5', _('Bigger')),
            ('fs-4', _('Big')),
            ('fs-3', _('Larger')),
            ('fs-2', _('Large')),
        ],
        default='',
        label=_('Tabs font size'),
    )
    tabs_orientation = ChoiceBlock(
        required=False,
        choices=[
            ('', _('Horizontal')),
            ('flex-column', _('Vertical')),
        ],
        default='',
        label=_('Tabs orientation'),
    )
    tabs_justify = ChoiceBlock(
        required=True,
        choices=[
            ('justify-content-start', _('Align left')),
            ('justify-content-center', _('Align center')),
            ('justify-content-end', _('Align right')),
        ],
        default='justify-content-start',
        label=_('Tabs horizontal alignment'),
    )
    # tabs_close = BooleanBlock(
    #     required=False,
    #     label=_('Show close button'),
    #     help_text=_('Allows to collapse sidebar and use full page with for content.'),
    # )
    items = TabItemsBlock()
    
    class Meta:
        icon = 'sidebar-tabs'
        label = _('Sidebar tabs')
        template = 'waggylabs/blocks/template/sidebar_tabs.html'
        form_template = 'waggylabs/blocks/form_template/sidebar_tabs.html'
        label_format = _('Sidebar: {items}')
        
        
class SidebarTabsBlock(WrapperBlock):
    """Sidebar iten with tabs for the the page. Tabs can contain
    contents (generated from headers on page), page visuals."""
    item = SidebarTabsItemBlock()
    
    class Meta:
        icon = 'sidebar-tabs'
        label = _('Sidebar tabs')
        help_text = _('Choose the style of the sidebar and which panels to use. '
                      'Note that some settings are incompartible. If tabs style is '
                      '"Tabs", then only link styles will be used for titles. '
                      'Vertical orientation of tab buttons does not support "Tabs" '
                      'style. When blocks are rendered within tabs, their header '
                      'text and icon becomes the tab header and icon, while the '
                      'header style is ignored.')