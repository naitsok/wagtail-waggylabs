from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.search import index

from wagtailmenus.models import MenuPageMixin
from wagtailmenus.panels import menupage_panel

from waggylabs.blocks.base_body import BaseBodyBlock
from waggylabs.models.base_page import BasePage


class SitePage(BasePage, MenuPageMixin):
    """A generic site page to contain content pages,
    such as Home, About, Research, Publications, etc.
    It can also list and filter posts if the site is used as a blog.
    """

    page_description = _('A generic site page to contain content, '
                        'such as Home, About, Research, Publications, etc.')
    template = 'waggylabs/pages/base_page.html'

    # Common fields

    show_in_menus_default = True

    # Database fields
    body = StreamField(
        BaseBodyBlock(),
        use_json_field=True,
    )

    # Search index configuration

    search_fields = BasePage.search_fields + [
        index.SearchField('body', partial_match=True, boost=2),
        index.AutocompleteField('body', boost=2),
    ]

    # Editor panels configuration
    
    content_panels = BasePage.content_panels + [
        FieldPanel('body'),
    ]
    promote_panels = BasePage.promote_panels + [
        menupage_panel,
    ]
    settings_panels = BasePage.settings_panels
    
    # Parent page / subpage type rules
    
    parent_page_types = ['wagtailcore.Page', 'waggylabs.SitePage']
    subpage_types = ['waggylabs.SitePage', 'waggylabs.PostListPage']