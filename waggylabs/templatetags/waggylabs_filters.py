
from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter

from urllib.parse import urlparse

from wagtailmarkdown.utils import render_markdown

from waggylabs.utils import pk_to_markdown
from waggylabs.widgets import BOOTSTRAP_ICONS


register = template.Library()


@register.filter(name='is_icon')
@stringfilter
def is_icon(value):
    """Checks if valus is in icons keys."""
    return value in BOOTSTRAP_ICONS


@register.filter(name='icon_class')
@stringfilter
def icon_class(value):
    """Gets Font Awesome icon class from its name."""
    return BOOTSTRAP_ICONS[value]


@register.filter(name='link_https')
@stringfilter
def link_https(value):
    """Checks the presence of http and https."""
    value = value.lower()
    if not (value.startswith('http://') or value.startswith('https://')):
        value = 'https://' + value
    return value

@register.filter(name='link_domain')
@stringfilter
def link_domain(value):
    """Gets domain name from URL."""
    domain = urlparse(value).netloc.lower()
    return domain.split('.')[0].title()
    

@register.filter(name='col_class')
def col_class(value):
    """Calulates the correct value for Bootstrap CSS
    column width class."""
    return int(12 / len(value.bound_blocks))


@register.filter(name='markdown')
def markdown(value, arg=None):
    """Returns the markdown with label, ref, eqref, cite
    updated with page primary key if it arg is not empty."""
    if arg:
        value = pk_to_markdown(value, arg)
    return render_markdown(value)
    