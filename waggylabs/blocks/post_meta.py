from django.utils.translation import gettext_lazy as _

from wagtail.blocks import (
    StructBlock, BooleanBlock, CharBlock
)

from waggylabs.blocks.icon import IconBlock, IconLocationBlock
from waggylabs.blocks.styling import (
    LinkStyleChoiceBlock, TextStyleChoiceBlock, CardStyleChoiceBlock,
    TextAlignmentChoiceBlock, HeaderStyleChoiceBlock
)

class SiblingPostBlock(StructBlock):
    """Defines the appearance of previous and next posts in
    the post footer block."""
    style = CardStyleChoiceBlock(
        label=_('Block style'),
    )
    header = CharBlock(
        required=False,
        label=_('Header: e.g. "Next post"'),
    )
    header_icon = IconBlock(
        label=_('Header icon'),
    )
    header_icon_location = IconLocationBlock(
        label=_('Header icon location'),
    )
    alignment = TextAlignmentChoiceBlock(
        label=_('Text alignment'),
    )
    post_link_style = LinkStyleChoiceBlock(
        label=_('Post link style'),
    )
    
    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(local_blocks, **kwargs)
        for block in self.child_blocks.values():
            block.field.widget.attrs.update({
                'placeholder': block.label,
            })

    class Meta:
        icon = 'post-meta'
        form_template = 'waggylabs/blocks/form_template/sibling_post.html'

class PostMetaBlock(StructBlock):
    """Post meta block describes post metadata, e.g. post author,
    post siblings, tags, categories. If it is las block in BodyBlock,
    then it is displayed after references."""
    header = CharBlock(
        required=False,
        label=_('Header'),
    )
    header_style = HeaderStyleChoiceBlock(
        label=_('Header style'),
    )
    header_icon = IconBlock(
        label=_('Header icon'),
    )
    header_icon_location = IconLocationBlock(
        label=_('Header icon location'),
    )
    style = CardStyleChoiceBlock(
        label=_('Block style'),
    )
    alignment = TextAlignmentChoiceBlock(
        label=_('Text alignment'),
    )
    show_categories = BooleanBlock(
        required=False,
        default=True,
        label=_('Show post categories'),
    )
    categories_header = CharBlock(
        required=False,
        label=_('Categories header'),
        help_text=_('Text to display before categories list.')
    )
    categories_header_style = TextStyleChoiceBlock(
        required=False,
        label=_('Categories header style'),
    )
    categories_style = LinkStyleChoiceBlock(
        required=False,
        label=_('Categories link style')
    )
    show_tags = BooleanBlock(
        required=False,
        default=True,
        label=_('Show post tags'),
    )
    tags_header = CharBlock(
        required=False,
        label=_('Tags header'),
        help_text=_('Text to display before tag list.'),
    )
    tags_header_style = TextStyleChoiceBlock(
        required=False,
        label=_('Tags header style'),
    )
    tags_style = LinkStyleChoiceBlock(
        required=False,
        label=_('Tags link style'),
    )
    show_sibling_posts = BooleanBlock(
        required=False,
        default=True,
        label=_('Show previous and next posts'),
        help_text=_(
            'Shows previous and next posts for the current post. '
            'Previous means either previously (chronologically) published or '
            'previous post from the series. Next means either (chronologically) '
            'published next or next post from the series.'
        ),
    )
    previous_post = SiblingPostBlock(
        label=_('Previous post'),
    )
    next_post = SiblingPostBlock(
        label=_('Next post'),
    )
    
    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(local_blocks, **kwargs)
        for block in self.child_blocks.values():
            if block.name != 'previous_post' and block.name != 'next_post':
                block.field.widget.attrs.update({
                    'placeholder': block.label,
                })
    
    def render(self, value, context):
        value['show_categories_tags'] = value['show_categories'] and \
            value['show_tags'] and context['page'].post_categories.count() > 0 and \
                context['page'].tags.count() > 0
        value['show_header'] = value['categories_header'] or value['tags_header']
        value['dd_width'] = 'col-sm-9' if value['show_header'] else 'col-sm-12'
        value['show_sibling_posts'] = value['show_sibling_posts'] and \
            ('previous_post' in context or 'next_post' in context)
        value['next_post_style'] = value['next_post']['style']
        
        return super().render(value, context)
    
    class Meta:
        label = _('Post metadata')
        icon = 'post-meta'
        template = 'waggylabs/blocks/template/post_meta.html'
        form_template = 'waggylabs/blocks/form_template/post_meta.html'
        help_text = _('Post metadata displays information '
                      'about the post, such as tags, categories, '
                      'links to previous and next posts. If this block '
                      'is at the end, it will be rendered after (possible) '
                      'references.')