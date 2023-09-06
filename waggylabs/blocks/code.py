from django.conf import settings
from django.utils.translation import gettext_lazy as _

from wagtail.blocks import ChoiceBlock, TextBlock, StructBlock

from wagtailmarkdown.blocks import render_markdown

# list of pairs for code block; first value must indicate the valid
# codemirror mode file (e.g., stex, clike, etc), https://codemirror.net/5/mode/;
# second value is the display text
CODEBLOCK_LANGS = getattr(
    settings,
    'WAGGYLABS_CODEBLOCK_LANGS',
    {
        # 'CodeMirror MIME type': ('CodeMirror mode folder', 'Pygments short name', 'Human readable name')
        # https://codemirror.net/5/mode/index.html
        # https://pygments.org/languages/
        'text/x-python': ('python', 'python', 'Python'),
        'text/x-csrc': ('clike', 'c', 'C'),
        'text/x-c++src': ('clike', 'cpp', 'C++'),
        'text/x-java': ('clike', 'java', 'Java/Kotlin'),
        'text/x-csharp': ('clike', 'csharp', 'C#'),
        'text/x-objectivec': ('clike', 'objectivec', 'Objective C'),
        'text/x-scala': ('clike', 'scala', 'Scala'),
        # 'text/x-django': ('django', 'django', 'Django template markup'), # Not working
        # 'text/x-dockerfile': ('dockerfile', 'dockerfile', 'Dockerfile'), # Not working
        'application/xml': ('xml', 'xml', 'XML'), # Needs to be before HTML mode
        'text/html': ('htmlmixed', 'html', 'HTML'),
        'text/javascript': ('javascript', 'javascript', 'Javascipt'),
        'text/json': ('javascript', 'json', 'JSON'),
        'text/typescript': ('javascript', 'typescript', 'TypeScript'),
        'text/x-mathematica': ('mathematica', 'mathematica', 'Mathematica'),
        'text/x-octave': ('octave', 'matlab', 'Matlab'),
        'application/x-powershell': ('powershell', 'powershell', 'Powershell'),
        # 'text/x-rsrc': ('r', 'r', 'R'),
        # 'text/x-rustsrc': ('rust', 'rust', 'Rust'), # Not working
        'text/x-sh': ('shell', 'bach', 'Bach/Shell'),
        'text/x-swift': ('swift', 'swift', 'Swift'),
        'text/x-sql': ('sql', 'sql', 'SQL'),
    }
)

class CodeBlock(StructBlock):
    """Code block to enter code with highlighting using CodeMirror editor. According to 
    https://docs.wagtail.org/en/stable/advanced_topics/customisation/streamfield_blocks.html#additional-javascript-on-structblock-forms.
    """
    
    mode = ChoiceBlock(
        choices=[(key, CODEBLOCK_LANGS[key][2]) for key in CODEBLOCK_LANGS.keys()],
        required=True,
        default='text/x-python',
        label=_('Code language'),
        help_text=_('Choose the programming language.'),
    )
    code = TextBlock(
        required=True,
        label=_('Code snippet'),
        help_text=_('Write or paste code.'),
    )
    
    def render_basic(self, value, context=None):
        if value['mode'] in CODEBLOCK_LANGS:
            return render_markdown('```' + CODEBLOCK_LANGS[value['mode']][1] +
                                '\n' + value['code'] +
                                '\n```', context)
        else:
            return render_markdown('```\n' + value['code'] + '\n```', context)
    
    class Meta:
        icon = 'code'
        label = _('Code')
        label_format = _('Code: {mode}')
    