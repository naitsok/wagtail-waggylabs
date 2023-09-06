from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from wagtail.admin.panels import Panel

class ReadOnlyPanel(Panel):
    
    """ ReadOnlyPanel EditHandler Class, adapted from https://github.com/wagtail/wagtail/issues/2893
        Usage:
        fieldname:          name of field to display
        style:              optional, any valid style string
        add_hidden_input:   optional, add a hidden input field to allow retrieving data in form_clean (self.data['field'])
        If the field name is invalid, or an error is received getting the value, empty string is returned.
        """
    def __init__(self, fieldname, style=None, add_hidden_input=False, *args, **kwargs):
        # error if fieldname is not string
        if type(fieldname)=='str':
            self.fieldname = fieldname
        else:
            try:
                self.fieldname = str(fieldname)
            except:
                pass
        self.style = style
        self.add_hidden_input = add_hidden_input
        super().__init__(*args, **kwargs)

    def clone(self):
        return self.__class__(
            fieldname=self.fieldname,
            heading=self.heading,
            help_text=self.help_text,
            style=self.style,
            add_hidden_input=self.add_hidden_input,
        )


    class BoundPanel(Panel.BoundPanel):
        """BoundPanel class of ReadOnlyPanel"""
        def get_value(self):
            # try to get the value of field, return empty string if failed
            try:
                value = getattr(self.instance, self.panel.fieldname)
                if callable(value):
                    value = value()
            except AttributeError:
                value = ''
            return value
        
        def render_html(self, parent_context):
            # return formatted field value
            self.value = self.get_value()
            return format_html('''<div class="w-field__input">
                               <div class="w-field__textoutput" role="textbox" tabindex="0">{}
                               </div>
                               </div>''', self.value)

        def render(self):
            # return formatted field value
            self.value = self.get_value()
            return format_html('''<div class="w-field__input">
                               <div class="w-field__textoutput" role="textbox" tabindex="0">{}
                               </div>
                               </div>''', self.value)

        def render_as_object(self):
            return format_html(
                '<fieldset>{}'
                '<ul class="fields"><li><div class="field">{}</div></li></ul>'
                '</fieldset>',
                self.panel.heading('legend'), self.render())

        def hidden_input(self):
            # add a hidden input field if selected, field value can be retrieved in form_clean with self.data['field']
            if self.panel.add_hidden_input:
                input = f'<input type="hidden" name="{self.panel.fieldname}" value="{self.value}" id="id_{self.panel.fieldname}">'
                return format_html(input)
            return ''

        def heading_tag(self, tag):
            # add the label/legend tags only if heading supplied
            if self.heading:
                if tag == 'legend':
                    return format_html('<legend>{}</legend>', self.panel.heading)
                return format_html('<label>{}{}</label>', self.panel.heading, ':')
            return ''

        def get_style(self):
            # add style if supplied
            if self.panel.style:
                return format_html('style="{}"', self.panel.style)
            return ''

        def render_as_field(self):
            # render the final output
            return format_html(
                '<div class="field" {}>'
                '{}'
                '<div class="field-content">{}</div>'
                '{}'
                '</div>',
                format_html(self.get_style()), self.heading_tag('label'), self.render(), self.hidden_input())