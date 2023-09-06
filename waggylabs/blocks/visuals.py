from django.utils.translation import gettext_lazy as _

from wagtail.blocks import StructBlock, CharBlock, BooleanBlock

from waggylabs.blocks.base_body import BaseBodyBlock
from waggylabs.blocks.icon import IconBlock, IconLocationBlock
from waggylabs.blocks.styling import LinkStyleChoiceBlock
from waggylabs.blocks.wrapper import WrapperBlock


class VisualsItemBlock(StructBlock):
    """BLock item to add thumbnails on visuals to sidebar.
    Embeds, equations, figures, listings, tables can be included."""
    preview_buttons_text = CharBlock(
        required=False,
        label=_('Preview buttons text'),
        
    )
    preview_buttons_icon = IconBlock(
        required=False,
        label=_('Preview buttons icon'),
    )
    preview_buttons_icon_location = IconLocationBlock(
        required=False,
        label=_('Preview buttons icon location'),
    )
    preview_buttons_style = LinkStyleChoiceBlock(
        required=False,
        label=_('Preview buttons style'),
    )
    include_embeds = BooleanBlock(
        required=False,
        label=_('Include embeds'),
    )
    include_equations = BooleanBlock(
        required=False,
        label=_('Include equations'),
    )
    include_figures = BooleanBlock(
        required=False,
        label=_('Include figures'),
    )
    include_listings = BooleanBlock(
        required=False,
        label=_('Include listings'),
    )
    include_tables = BooleanBlock(
        required=False,
        label=_('Include tables'),
    )
    
    def render(self, value, context):
        block_types = []
        for key, val in value.items():
            if 'include_' in key and val:
                block_types.append(key[8:-1])
        if value['include_tables']:
            block_types.append('table_figure')
        
        value['visuals'] = BaseBodyBlock.blocks_by_types(
            context['page'].body,
            block_types
        )
        
        return super().render(value, context)
    
    class Meta:
        icon = 'image'
        label = _('Visuals')
        template = 'waggylabs/blocks/template/visuals.html'
        form_template = 'waggylabs/blocks/form_template/visuals.html'


class VisualsBlock(WrapperBlock):
    """Block to display contents for post series. E.g. main post
    and its subposts."""
    item = VisualsItemBlock()
    
    class Meta:
        icon = 'image'
        label = _('Visuals')
        help_text = _('Adds sidebar block with the selected visuals. More than '
                      'one such block can be added with different visuals '
                      'selected. Selected visuals will appear as thumbnails '
                      'in the sidebar and open in a dialog box for the preview.')