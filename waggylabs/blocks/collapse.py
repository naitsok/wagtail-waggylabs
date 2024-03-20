
from django.utils.translation import gettext_lazy as _

from wagtail.blocks import (
    StreamBlock, StructBlock, CharBlock, StructValue
)

from waggylabs.blocks.blockquote import BlockQuoteBlock
from waggylabs.blocks.carousel import ImageCarouselBlock
from waggylabs.blocks.citation import CitationBlock
from waggylabs.blocks.document import DocumentBlock
from waggylabs.blocks.embed import EmbedBlock
from waggylabs.blocks.equation import EquationBlock
from waggylabs.blocks.figure import FigureBlock
from waggylabs.blocks.icon import IconBlock, IconLocationBlock
from waggylabs.blocks.styling import (
    LinkStyleChoiceBlock, CardStyleChoiceBlock, TextAlignmentChoiceBlock
)
from waggylabs.blocks.link_list import LinkListBlock
from waggylabs.blocks.listing import ListingBlock
from waggylabs.blocks.markdown import MarkdownBlock
from waggylabs.blocks.post_archive import PostArchiveBlock
from waggylabs.blocks.post_category_list import PostCategoryListBlock
from waggylabs.blocks.post_highlights import PostHighlightsBlock
from waggylabs.blocks.post_tag_list import PostTagListBlock
from waggylabs.blocks.table import TableBlock, TableFigureBlock


class CollapseContentBlock(StreamBlock):
    """Block to keep content of the collapse block."""
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
        label = _('Body of the collapse')
        
        
class CollapseBlock(StructBlock):
    """Collapse block to e.g. put content under spoiler."""
    text = CharBlock(
        required=False,
        label=_('Text on the button'),
    )
    icon = IconBlock(
        required=False,
        label=_('Button icon'),
    )
    icon_location = IconLocationBlock(
        required=False,
        label=_('Button icon location'),
    )
    button_style = LinkStyleChoiceBlock()
    style = CardStyleChoiceBlock(
        label=_('Block style'),
    )
    alignment = TextAlignmentChoiceBlock(
        label=_('Text alignment'),
    )
    
    body = CollapseContentBlock(requred=True)
    
    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(local_blocks, **kwargs)
        self.child_blocks['text'].field.widget.attrs.update({
            'placeholder': _('Text on the collapse button'),
        })
        
    @classmethod
    def blocks_by_types(cls, collapse: StructValue, types: list):
        """Returns blocks specificed by types (e.g., citation and document)
         ordered by the appearance in the CollapseBlock StructValue."""
        blocks_by_types = []
        for block in collapse.value['body']:
            if block.block_type in types:
                blocks_by_types.append(block)
        return blocks_by_types
        
    class Meta:
        icon = 'arrows-up-down'
        label = _('Collapse')
        form_template = 'waggylabs/blocks/form_template/collapse.html'
        template = 'waggylabs/blocks/template/collapse.html'
        label_format = _('Collapse: {text}')
