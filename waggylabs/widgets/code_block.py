from django import forms
from django.conf import settings
from django.utils.functional import cached_property

from wagtail.blocks.struct_block import StructBlockAdapter
from wagtail.telepath import register

from waggylabs.blocks.code import CodeBlock, CODEBLOCK_LANGS as CBL


CODEBLOCK_LANGS = getattr(settings, 'WAGGYLABS_CODEBLOCK_LANGS', CBL)
CODEBLOCK_LANGS = list(
    [
        f'waggylabs/vendor/codemirror/mode/{CODEBLOCK_LANGS[key][0]}/{CODEBLOCK_LANGS[key][0]}.js' 
        for key in CODEBLOCK_LANGS
    ]
)

class CodeBlockAdapter(StructBlockAdapter):
    """Telepath adapter for the CodeBlock. According to
    https://docs.wagtail.org/en/stable/advanced_topics/customisation/streamfield_blocks.html#additional-javascript-on-structblock-forms.
    """
    
    js_constructor = 'waggylabs.blocks.CodeBlock'
    

    @cached_property
    def media(self):
        structblock_media = super().media
        return forms.Media(
            js = structblock_media._js + [
                'waggylabs/vendor/codemirror/codemirror.min.js',
                'waggylabs/js/blocks/code-adapter.js',
                ] + CODEBLOCK_LANGS,
            css = {
                "all": (
                    'waggylabs/vendor/codemirror/codemirror.min.css',
                    'waggylabs/css/blocks/codemirror-tweaks.css',
                )
            }
        )

register(CodeBlockAdapter(), CodeBlock)
