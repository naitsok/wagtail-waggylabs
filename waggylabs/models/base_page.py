from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.admin import widgets
from wagtail.admin.panels import FieldPanel, HelpPanel, MultiFieldPanel
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.search import index

from hitcount.models import HitCountMixin, HitCount
from hitcount.views import HitCountMixin as ViewHitCountMixin

from wagtailmetadata.models import MetadataPageMixin

# from waggylabs.blocks.body import BaseBodyBlock
from waggylabs.blocks.sidebar import SidebarBlock
from waggylabs.panels import ReadOnlyPanel
from waggylabs.widgets import DisabledOptionSelect


class BasePage(MetadataPageMixin, Page, HitCountMixin):
    """BasePage class for the all the specific pages of WaggyLabs.
    Specific pages are SitePage, PostPage, etc. BasePage instances
    cannot be added directly in the Wagtail admin interface."""

    page_description = ''
    template = 'waggylabs/pages/base_page.html'
    
    # Common fields
    show_in_menus_default = True

    # Database fields
    title_style = models.CharField(
        blank=True,
        max_length=10,
        choices=[
            ('', _('Page title style')),
            ('h1', _('Header 1')),
            ('h2', _('Header 2')),
            ('h3', _('Header 3')),
            ('h4', _('Header 4')),
            ('h5', _('Header 5')),
            ('h6', _('Header 6')),
            ('display-1', _('Display header 1')),
            ('display-2', _('Display header 2')),
            ('display-3', _('Display header 3')),
            ('display-4', _('Display header 4')),
            ('display-5', _('Display header 5')),
            ('display-6', _('Display header 6')),
        ],
        default='',
        verbose_name=_('Page title style'),
    )
    
    # Hitcount
    hit_count_generic = GenericRelation(
        HitCount,
        object_id_field='pk',
        related_query_name='hit_count_relation',
    )
    
    # Content fields
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    # body field must be added for each subclass page
    # body field differs for each type of subclass page
    # body = StreamField(
    #     BaseBodyBlock(),
    #     use_json_field=True,
    # )
    
    # Content settings fields
    embed_caption_label = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Label for embeds'),
        help_text=_('For example, Embed. The label will be used to create '
                    'embed labels before caption. Leave empty for no label.'),
    )
    equation_caption_label = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Label for equations'),
        help_text=_('For example, Eqn. The label will be used to create '
                    'equatoion labels before caption. Note, that equation '
                    'labels are displayed only in preview dialogs. '
                    'Leave empty for no label.'),
    )
    figure_caption_label = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Label for figures'),
        help_text=_('For example, Figure. The label will be used to create '
                    'figure labels before caption. Leave empty for no label.'),
    )
    listing_caption_label = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Label for listings'),
        help_text=_('For example, Listing. The label will be used to create '
                    'listing labels before caption. Leave empty for no label.'),
    )
    table_caption_label = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Label for tables'),
        help_text=_('For example, Table. The label will be used to create '
                    'table labels before caption. Leave empty for no label.'),
    )
    show_sidebar = models.BooleanField(
        blank=True,
        default=False,
        verbose_name=_('Show sidebar'),
        help_text=_('Controls the display of sidebar.')
    )
    sidebar = StreamField(
        [
            ('sidebar', SidebarBlock()),
        ],
        max_num=1,
        blank=True,
        use_json_field=True
    )
    

    # Search index configuration

    search_fields = Page.search_fields + [
        index.SearchField('title', partial_match=True, boost=2),
        index.AutocompleteField('title', boost=2),
    ]

    # Widgets for panels
  
    datetime_widget = widgets.AdminDateTimeInput(
        attrs={
            'placeholder': 'YYYY-MM-DDThh:mm'
        }
    )

    # Editor panels configuration

    content_panels = Page.content_panels + [
        HelpPanel(content=_('The Body field allows to build a complex page with different content. '
                            'Editing, however, does show the final look of the page on the site. '
                            'To see the final version, use the "Preview" functionality below. '
                            'There are different blocks of the Body that can be used. '
                            'Heading block allows to set a heading of the certain level. '
                            'Paragraph is a simple rich text block that allows to interactively '
                            'make links to other site Pages, upload images and documents. '
                            'Note that images added in the block will not show in side panel '
                            'and will have nor caption nor reference. '),
                  heading=_('Tips for editing the Body field'),
                  classname='title'),
        ]
    
    promote_panels = Page.promote_panels + [
        MultiFieldPanel(
            [
                FieldPanel('created_at', heading='First created at', read_only=True),
                FieldPanel('first_published_at', heading='First published at', read_only=True),
                FieldPanel('last_published_at', heading='Last published at', read_only=True),
                ReadOnlyPanel('hit_counts', heading='Number of views'),
            ],
            heading=_('General information'),
        ),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('owner', permission='superuser'),
        FieldPanel('title_style', widget=DisabledOptionSelect),
        MultiFieldPanel(
            [
                FieldPanel('embed_caption_label'),
                FieldPanel('equation_caption_label'),
                FieldPanel('figure_caption_label'),
                FieldPanel('listing_caption_label'),
                FieldPanel('table_caption_label'),
            ],
            heading=_('Label settings'),
        ),
        MultiFieldPanel(
            [
                FieldPanel('show_sidebar'),
                FieldPanel('sidebar', classname='waggylabs-d-none'),
            ],
            heading=_('Sidebar settings'),
        ),
    ]
    
    # Parent page / subpage type rules
    # Empty parent_page_types prevents page creation in the
    # Wagtail admin editor interface
    parent_page_types = []
    subpage_types = []
    
    # Methods

    def hit_counts(self):
        """Displays hitcounts for the page if it has been created."""
        if self.pk is not None:
            # the page is created and hitcounts make sense
            return self.hit_count.hits
        else:
            return 0

    def serve(self, request, *args, **kwargs):
        hit_count = HitCount.objects.get_for_object(self)
        ViewHitCountMixin.hit_count(request, hit_count)
        return super().serve(request, *args, **kwargs)