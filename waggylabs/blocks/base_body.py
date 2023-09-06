
from django.utils.translation import gettext_lazy as _

from wagtail.blocks import StreamBlock
from wagtail.fields import StreamValue

from waggylabs.blocks.accordion import AccordionBlock
from waggylabs.blocks.blockquote import BlockQuoteBlock
from waggylabs.blocks.card_grid import CardGridBlock
from waggylabs.blocks.carousel import ImageCarouselBlock
from waggylabs.blocks.collapse import CollapseBlock
from waggylabs.blocks.columns import ColumnsBlock
from waggylabs.blocks.cut import CutBlock
from waggylabs.blocks.document import DocumentBlock
from waggylabs.blocks.citation import CitationBlock
from waggylabs.blocks.embed import EmbedBlock
from waggylabs.blocks.equation import EquationBlock
from waggylabs.blocks.figure import FigureBlock
from waggylabs.blocks.link_list import LinkListBlock
from waggylabs.blocks.listing import ListingBlock
from waggylabs.blocks.markdown import MarkdownBlock
from waggylabs.blocks.page_info import PageInfoBlock
from waggylabs.blocks.post_archive import PostArchiveBlock
from waggylabs.blocks.post_category_list import PostCategoryListBlock
from waggylabs.blocks.post_highlights import PostHighlightsBlock
from waggylabs.blocks.post_tag_list import PostTagListBlock
from waggylabs.blocks.table import TableBlock, TableFigureBlock


class BaseBodyBlock(StreamBlock):
    """General body field to add content to site pages and
     post pages."""
    accordion = AccordionBlock()
    blockquote = BlockQuoteBlock()
    card_grid = CardGridBlock()
    carousel = ImageCarouselBlock()
    collapse = CollapseBlock()
    columns = ColumnsBlock()
    citation = CitationBlock()
    cut = CutBlock()
    document = DocumentBlock()
    embed = EmbedBlock()
    equation = EquationBlock()
    figure = FigureBlock()
    link_list = LinkListBlock()
    listing = ListingBlock()
    page_info = PageInfoBlock()
    post_archive = PostArchiveBlock()
    post_category = PostCategoryListBlock()
    post_highlights = PostHighlightsBlock()
    post_tag_list = PostTagListBlock()
    table = TableBlock()
    table_figure = TableFigureBlock()
    text = MarkdownBlock()
    
    
    @classmethod
    def blocks_by_types(cls, body: StreamValue, types: list):
        """Returns blocks specificed by types (e.g., citation and document)
         ordered by the appearance in the body StreamValue
         (body = StreamField(BodyBlock())) in a Page model."""
        blocks_by_types = []
        for block in body:
            # Append all citation and document blocks
            if block.block_type in types:
                blocks_by_types.append(block)
            
            # If block is accordion - loop through its child blocks
            # and append the specified types of blocks
            if block.block_type == 'accordion':
                blocks_by_types = (blocks_by_types +
                                   AccordionBlock.blocks_by_types(block, types))
                
            # If block is collapse - loop through its child blocks
            # and append the specified types of blocks
            if block.block_type == 'collapse':
                blocks_by_types = (blocks_by_types +
                                   CollapseBlock.blocks_by_types(block, types))
            
            # If block is columns - loop through its child blocks
            # and append the specified types of blocks
            if block.block_type == 'columns':
                blocks_by_types = (blocks_by_types +
                                   ColumnsBlock.blocks_by_types(block, types))
        
        return blocks_by_types
    
    def render(self, value, context):
        if type(value) is not dict:
            value = { 'body': value }
            
        # if post_meta and page_info blocks are at the end of body
        # before them references must be rendered
        page_body = []
        info_meta = []
        for idx, block in enumerate(value['body']):
            if (idx >= len(value) - 2) and \
                (value['body'].raw_data[-1]['type'] in ['post_meta', 'page_info']) and \
                (block.block_type in ['post_meta', 'page_info']):
                info_meta.append(block)
            else:
                page_body.append(block)
                
        value = {
            'body': page_body,
            'info_meta': info_meta,
        }
            
        value['literature'] = BaseBodyBlock.blocks_by_types(
            value['body'],
            ['citation', 'document']
        )
        
        if context['page'].show_sidebar:
            value['modals'] = BaseBodyBlock.blocks_by_types(
                value['body'],
                ['embed', 'equation', 'listing', 'figure', 'table', 'table_figure']
            )
        
        if 'page_in_list' in context:
            # page is rendered in the list, e.g. after search
            # we need to display blocks in page.body only those that before cut
            # other blocks may be rendereded truncated, for example, to avoid image 
            # loading and use of traffic
            # however, literature, equations and all label blocks must be rendered
            # hidden in order to correctly generate reference and citations
            before_cut = []
            after_cut = []
            cut_met = False
            for block in value['body']:
                if not cut_met:
                    before_cut.append(block)
                else:
                    after_cut.append(block)
                if block.block_type == 'cut':
                    cut_met = True
            value['before_cut'] = before_cut
            value['after_cut'] = after_cut
            
        return super().render(value, context)
    
    class Meta:
        icon = 'doc'
        label = _('Page content')
        template = 'waggylabs/blocks/template/base_body.html'
        block_counts = {
            'cut': { 'max_num': 1 },
        }