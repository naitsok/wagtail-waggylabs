
import json
import os
import re

from collections import OrderedDict

from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _


def collect_icons():
    """Collects icon classes from the CSS file."""
    icons_css_path = os.path.join(settings.STATIC_ROOT, 'waggylabs/vendor/bootstrap/bootstrap-icons-input.css')
    if not os.path.exists(icons_css_path):
        icons_css_path = os.path.join(
            settings.BASE_DIR,
            'waggylabs/static/waggylabs/vendor/bootstrap/bootstrap-icons-input.css'
        )
    with open(icons_css_path, 'r') as f:
        matches = [m.group(0).lstrip('.').rstrip(':')
                for m in re.finditer(r'\.bi-[a-z\-]*\:', f.read())]
    matches.sort()
    d = OrderedDict()
    for m in matches:
        d[m[3:].replace('-', ' ')] = 'bi ' + m
    return d


BOOTSTRAP_ICONS = collect_icons()
class IconInput(forms.TextInput):
    """Widget to select Bootstrap icon.
    See https://www.cssscript.com/tiny-fast-autocomplete/
    """
    template_name = 'waggylabs/widgets/input_cross_button.html'
    
    def __init__(self,
                 icons=BOOTSTRAP_ICONS,
                 attrs={
                     'placeholder': _('Icon - start typing'),
                     'class': 'autocomp',
                 }):
        self.icons = icons
        super().__init__(attrs)
        
    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs['data-controller'] = 'icon'
        attrs['data-icon-icons-value'] = json.dumps(self.icons)
        return attrs
    
    @property
    def media(self):
        return forms.Media(
            js=[
                # load the UI library
                "waggylabs/vendor/autocomp/autocomp.min.js",
                # load controller JS
                "waggylabs/js/widgets/icon-controller.js",
            ],
            css={"all": [
                "waggylabs/vendor/autocomp/autocomp.min.css",
                "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/bootstrap-icons.min.css",
                ]},
        )
        