from django import forms
from django.utils.translation import gettext_lazy as _

from wagtail.admin.forms.auth import LoginForm

from captcha.fields import CaptchaField


class CaptchaLoginForm(LoginForm):
    """Adds captcha field to wagtail admin login form."""

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.fields['captcha'] = CaptchaField()
        self.fields['captcha'].widget.attrs['placeholder'] = _('Solve me')

    # def get_invalid_login_error(self):
    #     return forms.ValidationError(
    #         self.error_messages['invalid_login'],
    #         code='invalid_login',
    #         params={'username': 'email'},
    #     )