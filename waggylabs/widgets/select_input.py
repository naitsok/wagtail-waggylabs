
from django import forms


class DisabledOptionSelect(forms.widgets.Select):
    """Select with disabled option, which value equals to
    empty string."""
    option_template_name = 'waggylabs/widgets/select_option.html'