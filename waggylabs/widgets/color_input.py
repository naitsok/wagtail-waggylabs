
from django import forms

from wagtail.utils.widgets import WidgetWithScript


class ColorInput(WidgetWithScript, forms.widgets.HiddenInput):
    """Widget to select color."""
    template_name = 'waggylabs/widgets/color_input.html'
    
    def __init__(
        self,
        attrs={
            'class': 'waggylabs-color-input',
        }):
        super().__init__(attrs)
        
    def render_js_init(self, id_, name, value):
        """Attaches javascript init function to the widget."""
        return f'colorAttach("{id_}");'
    
    @property
    def media(self):
        return forms.Media(
            js=(
                "waggylabs/js/widgets/color-input.js",
            )
        )