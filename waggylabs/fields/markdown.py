from django.db.models import TextField

from waggylabs.widgets import MarkdownTextarea


class MarkdownField(TextField):
    """A replacement of WagtailMarkdown MarkdownField
    to use MarkdownTextarea of WaggyLabs."""
    def formfield(self, **kwargs):
        defaults = { 'widget': MarkdownTextarea }
        defaults.update(kwargs)
        return super().formfield(**defaults)