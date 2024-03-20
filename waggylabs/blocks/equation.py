import re

from django.utils.translation import gettext_lazy as _

from wagtail.blocks import StructBlock

from waggylabs.blocks.markdown import MarkdownBlock
from waggylabs.blocks.label import LabelBlock


class EquationBlock(StructBlock):
    """A standalone equation block with (skippable) caption. Edit equation via CodeMirror with LaTeX mode. According to 
    https://docs.wagtail.org/en/stable/advanced_topics/customisation/streamfield_blocks.html#additional-javascript-on-structblock-forms.
    """
    equation = MarkdownBlock(
        required=True,
        help_text=_('Write or paste LaTeX style equation (equation, '
                    'matrix, align, etc. environments are supported). '),
        min_height='150px',
        max_height='150px',
        stex_combine='false',
        toolbar=('subscript,superscript,equation,matrix,'
                                'align,multiline,split,gather,alignat,'
                                'flalign,|,preview,side-by-side,fullscreen'),
        statusbar='false',
    )
    caption = MarkdownBlock(
        required=False,
        label=_('Equation caption'),
        help_text=_('Caption that will be displayed when the equation is shown '
                    'in the dialog box or in the sidebar.'),
        min_height='100px',
        max_height='100px',
        stex_combine='true',
        toolbar=('bold,italic,strikethrough,|,unordered-list,'
                                'ordered-list,link,|,code,subscript,superscript,|,'
                                'preview,side-by-side,fullscreen,guide'),
        statusbar='false',
    )
    label = LabelBlock(
        max_length=50,
        required=False,
        form_classname='waggylabs-label-equation',
        help_text=_('Label for the current equation to be used in the markdown block '
                    'for referencing using standard LaTeX \\\u3164ref{...} syntax. '
                    'This label will be added only if no \\\u3164label{...} is found '
                    'within the \\\u3164begin{...}...\\\u3164end{...} statement.'
                    'The final reference processing is happening on the published page, '
                    'which can be checked using "Preview" functionality.'),
    )
    
    def __init__(self, local_blocks=None, **kwargs):
        super().__init__(local_blocks, **kwargs)
        self.re_label = re.compile(r'\\label\{(.*?)\}', re.IGNORECASE)
        self.re_begin = re.compile(r'\\begin\{[\w]*?\}', re.IGNORECASE)
        self.re_end = re.compile(r'\\end\{[\w]*?\}', re.IGNORECASE)
    
    def render(self, value, context):
        """Renders the equation. If it is rendered in sidebar or modal,
        removes the numbering and label to avoid MathJax errors."""
        equation_string = value['equation'].lower()
        # First add LaTeX \begin{equation} and \end{equation}
        # if no \begin{...} and \end{...} statements are present
        if not equation_string.startswith('\\begin{'):
            value['equation'] = ('\\begin{equation}\n' +
                                 value['equation'].trim('$') +
                                 '\\end{equation}\n')
        # then check and add label if no \label{...} is found
        # within begin{...} and \end{...} statements
        equation_string = value['equation'].lower()
        if (not '\\label{' in equation_string) and value['label']:
            idx = equation_string.find('\\end{')
            value['equation'] = (value['equation'][:idx] +
                                    '\n\\label{' + value['label'] +
                                    '}\n' + value['equation'][idx:])
        # label within MathJax block must be correctly updated with page id
        value['equation'] = re.sub(self.re_label,
                                   lambda m: (
                                       r'\label{' + m.group(1) + '-' +
                                       str(context['page'].pk) + '}'
                                    ),
                                   value['equation'])
        # if equation is rendered in sidebar,
        # \label{...} must be removed to avoid MathJax label error
        # and * must be added to avoid equation numbering
        if (('sidebar' in context and context['sidebar']) or
            ('modal' in context and context['modal'])):
            value['equation'] = re.sub(self.re_label, '', value['equation'])
            value['equation'] = re.sub(self.re_begin,
                                       lambda m: m.group(0)[:-1] + '*}',
                                       value['equation'])
            value['equation'] = re.sub(self.re_end,
                                       lambda m: m.group(0)[:-1] + '*}',
                                       value['equation'])

        return super().render(value, context)
    
    class Meta:
        icon = 'equation'
        label = _('Equation')
        template = 'waggylabs/blocks/template/equation.html'
        label_format = _('Equation')