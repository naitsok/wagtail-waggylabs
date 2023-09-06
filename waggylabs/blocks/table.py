from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from wagtail.blocks import StructBlock
from wagtail.contrib.table_block.blocks import TableBlock as WagtailTableBlock
from wagtail.images.blocks import ImageChooserBlock

from waggylabs.widgets import TableInput

from waggylabs.blocks.markdown import MarkdownBlock
from waggylabs.blocks.label import LabelBlock


class TableFigureBlock(StructBlock):
    """Add Table as picture."""
    caption = MarkdownBlock(
        required=False,
        label=_('Table caption'),
        help_text=None,
        easymde_min_height='150px',
        easymde_max_height='150px',
        easymde_combine='true',
        easymde_toolbar_config=('bold,italic,strikethrough,|,unordered-list,'
                                'ordered-list,link,|,code,subscript,superscript,|,'
                                'preview,side-by-side,fullscreen,guide'),
        easymde_status='false',
    )
    image = ImageChooserBlock(
        required=True,
        label='Table image',
        # help_text=_('Choose an image'),
        )
    footer = MarkdownBlock(
        required=False,
        label=_('Table footer'),
        help_text=None,
        easymde_min_height='100px',
        easymde_max_height='100px',
        easymde_combine='true',
        easymde_toolbar_config=('bold,italic,strikethrough,|,unordered-list,'
                                'ordered-list,link,|,code,subscript,superscript,|,'
                                'preview,side-by-side,fullscreen,guide'),
        easymde_status='false',
    )
    label = LabelBlock(
        max_length=50,
        required=False,
        form_classname='waggylabs-label-table', # needed to render references to tables
    )
    
    class Meta:
        template = 'waggylabs/blocks/template/table_figure.html'
        icon = 'table'
        label = _('Table as picture')
        label_format = _('Table: {image}')


DEFAULT_TABLE_OPTIONS = {
    'minSpareRows': 0,
    'startRows': 3,
    'startCols': 3,
    'colHeaders': False,
    'rowHeaders': False,
    'contextMenu': [
        'row_above',
        'row_below',
        '---------',
        'col_left',
        'col_right',
        '---------',
        'alignment',
        '---------',
        'remove_row',
        'remove_col',
        '---------',
        'undo',
        'redo'
    ],
    'editor': 'text',
    'stretchH': 'all',
    'height': 108,
    'renderer': 'text',
    'autoColumnSize': False,
}


# CSS classes for alignment in the table cells
# that map the classes of the Handsontable
LEFT = 'htLeft'
CENTER = 'htCenter'
RIGHT = 'htRight'
JUSTIFY = 'htJustify'
TOP = 'htTop'
MIDDLE = 'htMiddle'
BOTTOM = 'htBottom'
DEFAULT_ALIGN_CLASSES = {
    LEFT: 'text-start',
    CENTER: 'text-center',
    RIGHT: 'text-end',
    JUSTIFY: 'text-center',
    TOP: 'align-top',
    MIDDLE: 'align-middle',
    BOTTOM: 'align-bottom',
}


class BareTableBlock(WagtailTableBlock):
    """A replacement of Wagtail TableBlock with the table block with hidden caption and 
    cell text alignment."""
    def __init__(
        self,
        required=True,
        help_text=None,
        table_options=(settings.WAGGYLABS_TABLE_OPTIONS if 
                 hasattr(settings, 'WAGGYLABS_TABLE_OPTIONS') 
                 else DEFAULT_TABLE_OPTIONS),
        align_classes=(settings.WAGGYLABS_TABLE_ALIGN_CLASSES if 
                 hasattr(settings, 'WAGGYLABS_TABLE_ALIGN_CLASSES') 
                 else DEFAULT_ALIGN_CLASSES),
        keep_table_tag=True, # needed to skip table tag when rendering as part of a StructBlock
        **kwargs
    ):
        self.align_classes = align_classes
        self.keep_table_tag = keep_table_tag
        super().__init__(required, help_text, table_options, **kwargs)
        
    @cached_property
    def field(self):
        return forms.CharField(
            widget=TableInput(table_options=self.table_options),
            **self.field_options
        )
    
    def render(self, value, context=None):
        """Replaces Wiagtail render method to replace Hadsontable CSS align
        classes with Bootstrap CSS classes."""
        template = getattr(self.meta, "template", None)
        if template and value:
            table_header = (
                value["data"][0]
                if value.get("data", None)
                and len(value["data"]) > 0
                and value.get("first_row_is_table_header", False)
                else None
            )
            first_col_is_header = value.get("first_col_is_header", False)

            if context is None:
                new_context = {}
            else:
                new_context = dict(context)

            new_context.update(
                {
                    "self": value,
                    self.TEMPLATE_VAR: value,
                    "table_header": table_header,
                    "first_col_is_header": first_col_is_header,
                    "html_renderer": self.is_html_renderer(),
                    "table_caption": value.get("table_caption"),
                    "data": value["data"][1:]
                    if table_header
                    else value.get("data", []),
                    "keep_table_tag": self.keep_table_tag,
                }
            )

            if value.get("cell"):
                new_context["classnames"] = {}
                for meta in value["cell"]:
                    if "className" in meta:
                        new_context["classnames"][(meta["row"], meta["col"])] = self.align_classes[meta[
                            "className"
                        ]]

            return render_to_string(template, new_context)
        else:
            return self.render_basic(value or "", context=context)
    
    class Meta:
        default = None
        template = 'waggylabs/blocks/template/bare_table.html'
        icon = 'table'


class TableBlock(StructBlock):
    """Table block with caption provided by markdown block."""
    caption = MarkdownBlock(
        required=False,
        label=_('Table caption'),
        help_text=None,
        easymde_min_height='100px',
        easymde_max_height='100px',
        easymde_combine='true',
        easymde_toolbar_config=('bold,italic,strikethrough,|,unordered-list,'
                                'ordered-list,link,|,code,subscript,superscript,|,'
                                'preview,side-by-side,fullscreen,guide'),
        easymde_status='false',
    )
    table = BareTableBlock(
        required=True,
        label=_('Table data'),
        help_text=_('Columns and rows can be added via context menu appearing on '
                    'the right click. Markdown inside cells is supported. Inline '
                    'LateX equations can be added using $...$ pattern.'),
        keep_table_tag=False,
        # table_options = None, # see https://github.com/wagtail/wagtail/blob/main/wagtail/contrib/table_block/blocks.py
    )
    footer = MarkdownBlock(
        required=False,
        label=_('Table footer'),
        help_text=None,
        easymde_min_height='100px',
        easymde_max_height='100px',
        easymde_combine='true',
        easymde_toolbar_config=('bold,italic,strikethrough,|,unordered-list,'
                                'ordered-list,link,|,code,subscript,superscript,|,'
                                'preview,side-by-side,fullscreen,guide'),
        easymde_status='false',
    )
    label = LabelBlock(
        max_length=50,
        required=False,
        form_classname='waggylabs-label-table', # needed to render references to tables
    )
    
    class Meta:
        template = 'waggylabs/blocks/template/table.html'
        icon = 'table'
        label = _('Table')
        label_format = _('Table')