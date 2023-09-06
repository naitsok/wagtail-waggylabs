import re
import uuid

from bs4 import BeautifulSoup
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=False)
def random_uuid():
    """Django template tag to generate unique identifier
    needed for the HTML element ids, e.g. in Carousel block.

    Returns:
        str: unique identifier
    """
    return str(uuid.uuid4())


@register.simple_tag(takes_context=False)
def navbar_class(site_settings):
    """Generates CSS classes based on WaggyLabsSettings 
    for the <header> element containing navigation bar"""
    css_class = 'navbar navbar-expand-lg'
    if (not site_settings.theme_supports_color_mode
        and site_settings.navbar_theme):
        # if the upladed CSS theme does not support color modes,
        # add correct classes to have either light or dark navigation
        # bar dependinh on the navbar_theme setting
        css_class = (css_class +
                     ' navbar-' + site_settings.navbar_theme +
                     ' bg-' + site_settings.navbar_theme)
        
    if not site_settings.navbar_color:
        # if specific color has not been selected
        # add the default color and class
        # works only for Bootsrap 5.3 and higher
        # which has the bg-body-tertiary CSS class
        css_class = css_class + ' bg-body-tertiary'
        
    css_class = css_class + ' ' + site_settings.navbar_placement
    
    return css_class


@register.simple_tag(takes_context=False)
def main_class(site_settings, page):
    """Generates CSS class for the <main> element 
    depending on the WaggyLabsSettings and page sidebar."""
    
    if hasattr(page, 'show_sidebar'): # check needed when there is default HomePage
        if site_settings.constant_content_width or (page is not None and page.show_sidebar):
            if site_settings.content_width == 'narrow':
                return 'col-md-5 offset-md-2' # and col-md-3 for sidebar
            if site_settings.content_width == 'medium':
                return 'col-md-6 offset-md-1' # and col-md-4 for sidebar
            if site_settings.content_width == 'wide':
                return 'col-md-8' # and col-md-4 for sidebar
    
    if site_settings.content_width == 'narrow':
        return 'col-md-8 offset-md-2'
    if site_settings.content_width == 'medium':
        return 'col-md-10 offset-md-1'
    if site_settings.content_width == 'wide':
        return 'col-md-12'
    
    
@register.simple_tag(takes_context=False)
def sidebar_class(site_settings, page):
    """Generates CSS class for the sidebar <div> element
    depending on the WaggyLabsSettings and page sidebar."""
    css_class = ''
    if site_settings.content_width == 'narrow':
        css_class = 'col-md-3' # and col-md-3 for sidebar
    else:
        css_class = 'col-md-4'
    if page is None or not page.show_sidebar:
        css_class = css_class + ' d-none'
    return css_class


@register.simple_tag(takes_context=False)
def search_results_title(page, tokens):
    """Highlights parts of the title that match with tokens
    to highlight search results."""
    title = escape(page.title)
    for token in tokens:
        title = re.sub(
            token,
            lambda m: '<mark>' + m.group(0) + '</mark>',
            title,
            flags=re.IGNORECASE
        )
    return mark_safe(title)


@register.simple_tag(takes_context=False)
def search_results_body(page, tokens):
    """Highlights parts of the body that match with tokens
    to highlight search results."""
    body_rendered = page.body.stream_block.render_basic(page.body, context={'page': page})
    bs = BeautifulSoup(body_rendered, features='html.parser')
    body_text = bs.get_text()
    text_chunks = []
    for token in tokens:
        for match in re.finditer(token, body_text, flags=re.IGNORECASE):
            text_chunk = '<p>'
            (start, end) = match.span(0)
            
            if start - 200 < 0:
                start = 0
            else:
                text_chunk = '<p>...'
                
            text_chunk = text_chunk + \
                body_text[start:end + 200 + 11].replace(
                    match.group(0),
                    '<mark>' + match.group(0) + '</mark>'
                )
                
            if end + 200 > len(body_text):
                text_chunk = text_chunk + '</p>'
            else:
                text_chunk = text_chunk + '...</p>'

            text_chunks.append(text_chunk)
        
    if text_chunks:
        return mark_safe(''.join(text_chunks))
    return body_text[0:200] + '...'
