from django.utils.translation import gettext_lazy as _

from wagtail.blocks import RegexBlock


class LabelBlock(RegexBlock):
    """LabelBlock to add labels to figures, tables, references, etc,
    for referencing them in e.g. Markdown text using standard LaTex
    \ref{...} syntax. LabelBlock adds the specific CSS class to the
    standard Wagtail CharBlock. The CSS class will be used to select
    all the LabelBlocks by javascript selector for reference processing
    for the final view of the page."""
    def __init__(self,
                 regex=r'^[a-zA-Z\:\-\_][^\s\\\/\{\}\[\]\(\)]*$',
                 required=False,
                 help_text=_('Label for the current entity (embed, figure, table, equation) '
                             'to be used in the markdown block for referencing using '
                             'standard LaTeX \\\u3164ref{...} syntax. The final reference '
                             'processing is happening on the published page, which can '
                             'be checked using "Preview" functionality.'),
                 max_length=50,
                 min_length=None,
                 validators=(),
                 error_messages={
                     'invalid': _('Label must not start with a number or contain spaces, '
                                  'slashes, and any type of brackets.')
                     },
                 form_classname='',
                 **kwargs):
        # A specific waggylabs-label class is added to make these label not processable by MathJax
        super().__init__(
            regex,
            required,
            help_text,
            max_length,
            min_length,
            error_messages,
            validators,
            form_classname=form_classname + ' waggylabs-label',
            **kwargs
        )
        self.field.widget.attrs.update({
            'placeholder': 'e.g. fig1, tbl2, or lst3',
        })