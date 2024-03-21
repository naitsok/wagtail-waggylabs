
import json

from django import forms


class ColorInput(forms.TextInput):
    """
    See https://coloris.js.org/
    """
    template_name = 'waggylabs/widgets/input_cross_button.html'

    def __init__(self, attrs=None, swatches=[], theme='pill', theme_mode='auto',
                 formatToggle='true', close_button='true', clear_button='true'):
        self.swatches = swatches
        self.theme = theme
        self.theme_mode = theme_mode
        self.formatToggle = formatToggle
        self.close_button = close_button
        self.clear_button = clear_button
        super().__init__(attrs=attrs)

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs['data-controller'] = 'color'
        attrs['data-color-swatches-value'] = json.dumps(self.swatches)
        attrs['data-color-theme-value'] = self.theme
        attrs['data-color-theme-mode-value'] = self.theme_mode
        attrs['data-color-format-toggle-value'] = self.formatToggle
        attrs['data-color-close-button-value'] = self.close_button
        attrs['data-color-clear-button-value'] = self.clear_button
        return attrs

    @property
    def media(self):
        return forms.Media(
            js=[
                # load the UI library
                "waggylabs/vendor/coloris/coloris.min.js",
                # load controller JS
                "waggylabs/js/widgets/color-controller.js",
            ],
            css={"all": ["waggylabs/vendor/coloris/coloris.min.css"]},
        )


# Deprecated WidgetWithScript
'''
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
'''
