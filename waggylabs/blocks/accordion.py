from django.utils.translation import gettext_lazy as _

from wagtail.blocks import (
    StreamBlock, StructBlock, CharBlock, ListBlock,
    BooleanBlock, ChoiceBlock, StructValue
    )

from waggylabs.widgets import DisabledOptionSelect

from waggylabs.blocks.blockquote import BlockQuoteBlock
from waggylabs.blocks.carousel import ImageCarouselBlock
from waggylabs.blocks.citation import CitationBlock
from waggylabs.blocks.document import DocumentBlock
from waggylabs.blocks.embed import EmbedBlock
from waggylabs.blocks.equation import EquationBlock
from waggylabs.blocks.figure import FigureBlock
from waggylabs.blocks.icon import IconBlock, IconLocationBlock
from waggylabs.blocks.link_list import LinkListBlock
from waggylabs.blocks.listing import ListingBlock
from waggylabs.blocks.markdown import MarkdownBlock
from waggylabs.blocks.post_archive import PostArchiveBlock
from waggylabs.blocks.post_category_list import PostCategoryListBlock
from waggylabs.blocks.post_highlights import PostHighlightsBlock
from waggylabs.blocks.post_tag_list import PostTagListBlock
from waggylabs.blocks.table import TableBlock, TableFigureBlock


class AccordionContentBlock(StreamBlock):
    """Content block for one accordion item."""
    blockquote = BlockQuoteBlock()
    carousel = ImageCarouselBlock()
    citation = CitationBlock()
    document = DocumentBlock()
    embed = EmbedBlock()
    equation = EquationBlock()
    figure = FigureBlock()
    link_list = LinkListBlock()
    listing = ListingBlock()
    post_archive = PostArchiveBlock()
    post_category = PostCategoryListBlock()
    post_highlights = PostHighlightsBlock()
    post_tag_list = PostTagListBlock()
    table = TableBlock()
    table_figure = TableFigureBlock()
    text = MarkdownBlock(
        required=False,
        help_text='',
        stex_combine='true',
        min_height='150px',
        max_height='150px',
        toolbar=('bold,italic,strikethrough,|,unordered-list,'
                                'ordered-list,link,|,code,subscript,superscript,|,'
                                'preview,side-by-side,fullscreen,guide'),
        statusbar='false'
    )
    
    class Meta:
        label = _('Body of the accordion item')
    

class AccordionItemBlock(StructBlock):
    """One accordion item block with heading."""
    heading = CharBlock(
        required=True,
        label=_('Item heading'),
        classname='full subtitle'
    )
    header_icon = IconBlock(
        required=False,
        label=_('Header icon'),
    )
    header_icon_location = IconLocationBlock(
        required=False,
        label=_('Header icon location'),
    )
    is_open = BooleanBlock(
        required=False,
        label=_('Item is displayed expanded')
    )
    body = AccordionContentBlock(
        required=False,
    )
    
    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(local_blocks, **kwargs)
        self.child_blocks['heading'].field.widget.attrs.update({
            'placeholder': _('Heading of the item'),
        })
    
    class Meta:
        icon = 'accordion'
        label = _('Item of the accordion')
        form_template = 'waggylabs/blocks/form_template/accordion_item.html'
        label_format = '{heading}'


class AccordionBlock(StructBlock):
    """Accordion block in which multiple accordion items can 
    be added."""
    
    style = ChoiceBlock(
        choices=[
            ('collapsible', _('Items collapse')),
            ('stays_open', _('Items stay open')),
        ],
        default='collapsible',
        label=_('Item collapse style'),
        help_text=_('Collapse items when new items opens or keep them open'),
        widget=DisabledOptionSelect
    )
    items = ListBlock(AccordionItemBlock())
    
    @classmethod
    def blocks_by_types(cls, accordion: StructValue, types: list):
        """Returns blocks specificed by types (e.g., citation and document)
         ordered by the appearance in the AccordionBlock StructValue."""
        blocks_by_types = []
        for accordion_item in accordion.value['items']:
            for acc_item_block in accordion_item['body']:
                if acc_item_block.block_type in types:
                    blocks_by_types.append(acc_item_block)
        return blocks_by_types

    class Meta:
        icon = 'accordion'
        label = _('Accordion')
        template = 'waggylabs/blocks/template/accordion.html'
        form_template = 'waggylabs/blocks/form_template/accordion.html'
        label_format = _('Accordion: {items}')
    