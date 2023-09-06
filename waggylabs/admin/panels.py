# panels.py defines custom Panels for admin editing interface.
# The name of the file is the same as in wagtial.admin github to keep it
# similar.

from django.forms.utils import pretty_name
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import Panel, HelpPanel


class ReadOnlyPanel2(HelpPanel):
    """Description"""
    def __init__(self, field_name, template="wagtailadmin/panels/help_panel.html", **kwargs):
        value = getattr(self.get_bound_panel().instance, field_name)
        if callable(value):
            value = value()
        super().__init__(value, template, **kwargs)


class ReadOnlyPanel(Panel):
    """The Panel to display fields that are marked as non editable.
    Taken from https://github.com/wagtail/wagtail/issues/2893.
    With many thanks to Bertrand Bordage."""
    def __init__(self, attr, *args, **kwargs):
        self.attr = attr
        self.content = ''
        super().__init__(*args, **kwargs)

    def clone(self):
        return self.__class__(
            attr=self.attr,
            heading=self.heading,
            classname=self.classname,
            help_text=self.help_text,
        )
        
    class BoundPanel(Panel.BoundPanel):
        def __init__(self, panel, instance, request, form):
            super().__init__(panel, instance, request, form)
            self.template_name = '' # self.panel.template
            self.content = self.panel.content

    def render(self):
        value = getattr(self.instance, self.attr)
        if callable(value):
            value = value()
        return format_html('<div style="padding-top: 1.2em;">{}</div>', value)

    def render_as_object(self):
        return format_html(
            '<fieldset><legend>{}</legend>'
            '<ul class="fields"><li><div class="field">{}</div></li></ul>'
            '</fieldset>',
            self.heading, self.render())

    def render_as_field(self):
        return format_html(
            '<div class="field">'
            '<label>{}{}</label>'
            '<div class="field-content">{}</div>'
            '</div>',
            self.heading, _(':'), self.render())


