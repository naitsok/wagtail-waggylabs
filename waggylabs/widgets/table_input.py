from django import forms
from django.utils.functional import cached_property
from django.utils.translation import gettext as _

from wagtail.admin.staticfiles import versioned_static
from wagtail.telepath import register
from wagtail.widget_adapters import WidgetAdapter


class TableInput(forms.HiddenInput):
    """Minor change for Wagtail TableInput to use WaggyLabs table.js file with
    default caption hidden."""
    def __init__(self, table_options=None, attrs=None):
        self.table_options = table_options
        super().__init__(attrs=attrs)

    @cached_property
    def media(self):
        return forms.Media(
            css={'all': [
                versioned_static('table_block/css/vendor/handsontable-6.2.2.full.min.css'),
                'waggylabs/css/widgets/handsontable-tweaks.css',
            ]},
            js=[
                versioned_static('table_block/js/vendor/handsontable-6.2.2.full.min.js'),
                'waggylabs/vendor/marked/marked.min.js',
                'waggylabs/js/widgets/table-input.js',
                'waggylabs/js/widgets/markdown-emoji.js',
            ]
        )


class TableInputAdapter(WidgetAdapter):
    js_constructor = 'waggylabs.widgets.TableInput'
    
    class Media:
        js = ["waggylabs/js/blocks/table-input-adapter.js"]

    def js_args(self, widget):
        strings = {
            "Row header": _("Row header"),
            "Table headers": _("Table headers"),
            "Display the first row as a header": _("Display the first row as a header"),
            "Display the first column as a header": _(
                "Display the first column as a header"
            ),
            "Column header": _("Column header"),
            "Display the first row AND first column as headers": _(
                "Display the first row AND first column as headers"
            ),
            "No headers": _("No headers"),
            "Which cells should be displayed as headers?": _(
                "Which cells should be displayed as headers?"
            ),
            "Table caption": _("Table caption"),
            "A heading that identifies the overall topic of the table, and is useful for screen reader users.": _(
                "A heading that identifies the overall topic of the table, and is useful for screen reader users."
            ),
            "Table": _("Table"),
        }

        return [
            widget.table_options,
            strings,
        ]


register(TableInputAdapter(), TableInput)
