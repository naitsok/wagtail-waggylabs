
from django.utils.translation import gettext_lazy as _

from wagtail.blocks import StructBlock
from wagtail.documents.blocks import DocumentChooserBlock

from waggylabs.blocks.label import LabelBlock

class DocumentBlock(StructBlock):
    """Block to add documents and cite them using \cite{...} syntax."""
    document = DocumentChooserBlock()
    label = LabelBlock(
        required=False,
        form_classname='waggylabs-label-cite',
        help_text=_('Cite documents using LaTeX \\cite{...} syntax in text markdown block.')
    )
    
    class Meta:
        icon = 'doc-empty'
        label = _('Document')
        template = 'waggylabs/blocks/template/document.html'
        label_format = _('Document: {document}')