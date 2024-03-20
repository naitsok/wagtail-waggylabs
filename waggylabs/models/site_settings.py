from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from modelcluster.models import ClusterableModel

from wagtail.fields import StreamField
from wagtail.admin.panels import (
    FieldPanel, HelpPanel, ObjectList, TabbedInterface, MultiFieldPanel
)
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting

from waggylabs.blocks.footer_menu import FooterMenuBlock
from waggylabs.blocks.link_list import FooterLinkListBlock
from waggylabs.blocks.links import ExternalLinkBlock, InternalLinkBlock
from waggylabs.blocks.post_archive import FooterPostArchiveBlock
from waggylabs.blocks.post_highlights import FooterPostHighlightsBlock
from waggylabs.widgets import IconInput, ColorInput


@register_setting
class WaggyLabsSettings(BaseSiteSetting, ClusterableModel):
    """Settings for Waggy Labs site to set navbar (or small brand) image, 
    navbar (brand) slogan, and controls if the Waggy Labs site name should appear in the navbar."""
    
    # Database fields
    # Settings related to the site name display
    site_icon = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text=_('Brand icon that appears in navigation bar and in the browser tab.'),
        verbose_name=_('Site icon'),
    )
    site_slogan = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Phrase, that appears in navbar on the right to the brand image.'),
        verbose_name=_('Slogan'),
    )
    show_site_name = models.BooleanField(
        default=True,
        help_text=_('Indicates if title of the Waggy Labs site appears in '
                    'navigation bar and in browser tab e.g., Page Title - Site Name.'),
        verbose_name=_('Show site name in navigation bar and browser tab'),
    )
    site_name_separator = models.CharField(
        max_length=10,
        blank=True,
        help_text=_('Separator for site name e.g., Page Title - '
                    'Site Name or Page Title : Site Name.'),
        verbose_name=_('Separator for the site name'),
    )
    class SiteNameAlignment(models.TextChoices):
        """Alignment choices for the site name in navbar: 
        before page title or after page title."""
        LEFT = 'before_title', _('Before page title')
        RIGHT = 'after_title', _('After page title')
    site_name_alignment = models.CharField(
        max_length=25,
        choices=SiteNameAlignment.choices,
        default=SiteNameAlignment.RIGHT,
        help_text=_('The alignment of site name: before or after page title.'),
        verbose_name=_('Site name alignment'),
    )
    
    # Theme and navigation bar style settings
    site_theme = models.FileField(
        blank=True,
        help_text=_('CSS file with theme to be used instead of default Bootstrap theme.'),
        verbose_name=_('Bootstrap CSS theme'),
    )
    theme_supports_color_mode = models.BooleanField(
        blank=True,
        default=True,
        help_text=_('If the CSS theme file suppots Bootstrap dark and light modes.'),
        verbose_name=_('CSS theme supports dark and light modes'),
    )
    menu_max_levels = models.IntegerField(
        blank=False,
        default=getattr(settings, 'WAGGYLABS_MENU_MAX_LEVELS', 1),
        verbose_name=_('Maximum number of menu levels'),
        help_text=_('Specifies how deep in the page hierarchy the menu '
                    'must be rendered, i.e. what is the level of depth to '
                    'render the dropdown submenus.'),
        validators=[
            MinValueValidator(
                1,
                message=_('Maximum number of menu levels '
                          'cannot be less than 1.')
            ),
        ],
    )
    menu_allow_repeating_parents = models.BooleanField(
        blank=True,
        default=getattr(settings, 'WAGGYLABS_MENU_MAX_LEVELS', 1),
        verbose_name=_('Repeat parent links in the dropdown submenus')
    )
    class NavbarTheme(models.TextChoices):
        """Navigation bar theme: dark or light. Correct choice needs to be 
        selected based on the selected CSS Bootstrap theme."""
        AUTO = '', _('Auto')
        LIGHT = 'light', _('Light')
        DARK = 'dark', _('Dark')
    # navbar_theme = models.CharField(
    #     max_length=25,
    #     choices=NavbarTheme.choices,
    #     default=NavbarTheme.AUTO,
    #     blank=True,
    #     help_text=_('Navigation bar color mode: auto, light or dark. '
    #                 'Auto mode changes according to the global color mode '
    #                 'selection. Light or dark mode keep the selected mode, '
    #                 'which isespecially useful if CSS does not support color '
    #                 'modes, or specific color for the navigation bar was selected. '
    #                 'Ignored if the uploaded CSS does not support color modes.'),
    #     verbose_name=_('Navigation bar color mode'),
    # )
    navbar_color = models.CharField(
        max_length=25,
        default='',
        blank=True,
        help_text=_('Choose a specific color and opacity for the navigation bar. '
                    'Leave empty (use "Clear" button) to use the default theme color.'),
        verbose_name=_('Navigation bar color'),
    )
    class NavbarLinkWeight(models.TextChoices):
        """Navigation bar link weight: specify text weights for menu links."""
        DEFAULT = '', _('Default')
        BOLD = 'fw-bold', _('Bold')
        BOLDER = 'fw-bolder', _('Bolder')
        SEMIBOLD = 'fw-semibold', _('Semibold')
        MEDIUM = 'fw-medium', _('Medium')
        NORMAL = 'fw-normal', _('Normal')
        LIGHT = 'fw-light', _('Light')
        LIGHTER = 'fw-lighter', _('Lighter')
        
    navbar_link_color = models.CharField(
        max_length=25,
        default='',
        blank=True,
        help_text=_('Specifies the color and opacity for the navigation bar links. '
                    'Leave empty (use "Clear" button) to use the default Bootstrap theme color.'),
        verbose_name=_('Navigation bar link color'),
    )
    navbar_hover_link_color = models.CharField(
        max_length=25,
        default='',
        blank=True,
        help_text=_('Specifies the color and opacity for the navigation bar links during hover. '
                    'Leave empty (use "Clear" button) to use the default Bootstrap theme color.'),
        verbose_name=_('Navigation bar hover link color'),
    )
    navbar_link_weight = models.CharField(
        max_length=25,
        choices=NavbarLinkWeight.choices,
        default=NavbarLinkWeight.DEFAULT,
        blank=True,
        help_text=_('Specifies the font weigth for the navigation bar links.'),
        verbose_name=_('Navigation bar link weight'),
    )
    navbar_active_link_color = models.CharField(
        max_length=25,
        default='',
        blank=True,
        help_text=_('Specifies the color and opacity for the navigation bar active links. '
                    'Leave empty (use "Clear" button) to use the default Bootstrap theme color.'),
        verbose_name=_('Navigation bar active link color'),
    )
    navbar_active_link_weight = models.CharField(
        max_length=25,
        choices=NavbarLinkWeight.choices,
        default=NavbarLinkWeight.DEFAULT,
        blank=True,
        help_text=_('Specifies the font weigth for the navigation bar active links.'),
        verbose_name=_('Navigation bar active link weight'),
    )
    
    class NavbarPlacement(models.TextChoices):
        """Navbar placement choices from the Bootstrap documentation: 
        default, sticky-top or fixed-top."""
        DEFAULT = '', _('Default')
        STICKY_TOP = 'sticky-top', _('Sticky top')
        # FIXED_TOP = 'fixed-top', _('Fixed top')
    navbar_placement = models.CharField(
        max_length=10,
        choices=NavbarPlacement.choices,
        default=NavbarPlacement.DEFAULT,
        blank=True,
        help_text=_('Navigation bar placement options: default, '
                    'sticky-top or fixed-top. See Bootstrap documentation.'),
        verbose_name=_('Navigation bar menu placement')
    )
    class NavbarMenuAlignment(models.TextChoices):
        """Alignment of the menu in the navigation bar."""
        LEFT = 'left', _('Left')
        MIDDLE = 'middle', _('Middle')
        RIGHT = 'right', _('Right')
    navbar_menu_alignment = models.CharField(
        max_length=10,
        choices=NavbarMenuAlignment.choices,
        default=NavbarMenuAlignment.LEFT,
        blank=False,
        help_text=_('Menu links alignment in the navigation bar.'),
        verbose_name=_('Navigation bar menu alignment'),
    )
    
    # Navigation bar links to e.g. social media accounts
    navbar_links = StreamField([
        ('external_link', ExternalLinkBlock()),
        ('internal_link', InternalLinkBlock()),
    ], blank=True, use_json_field=True, verbose_name=_('Navigation bar links'))
    
    # Content settings
    class ContentWidth(models.TextChoices):
        """Width of the main content. Final width depends on the presence of
        the sidebar. See waggylabs_tags.py for width calculation."""
        NARROW = 'narrow', _('Narrow')
        MEDIUM = 'medium', _('Medium')
        WIDE = 'wide', _('Wide')
    content_width = models.CharField(
        max_length=10,
        choices=ContentWidth.choices,
        default=ContentWidth.MEDIUM,
        blank=False,
        help_text=_('Sets the width of the main content of any page. '
                    'Final width depends on the presence of a sidebar on '
                    'a particlar page.'),
        verbose_name=_('Page content width'),
    )
    constant_content_width = models.BooleanField(
        blank=True,
        default=False,
        help_text=_('Keep the width of the page content always the same '
                    'indepent from presence or absence of sidebar on the page. '
                    'If true, when the sidebar is not present on the page, '
                    'its place stays empty without change of page content width.'),
        verbose_name=_('Keep content width constant'),
    )
    
    # Footer settings
    copyright_icon = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Icon to used in front of the copyright phrase.'),
        verbose_name=_('Copyright icon'),
    )
    copyright_info = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Information about the copyright holder.'),
        verbose_name=_('Copyright information'),
    )
    content_license_link = models.URLField(
        blank=True,
        help_text=_('Link to the license for the content. For example, '
                    'to link to CC BY 3.0 license text.'),
        verbose_name=_('Link to content license'),
    )
    content_license_text = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Text to put for the license link'),
        verbose_name=_('Text of the license link'),
    )
    footer = StreamField(
        [
            ('footer_menu', FooterMenuBlock()),
            ('link_list', FooterLinkListBlock()),
            ('post_archive', FooterPostArchiveBlock()),
            ('post_highlights', FooterPostHighlightsBlock()),
        ],
        block_counts={
            'footer_menu': { 'max_num': 1 },
        },
        blank=True,
        use_json_field=True,
    )
    
    # Search settings
    search_in_menu = models.BooleanField(
        blank=True,
        default=True,
        verbose_name=_('Show search button in the menu'),
    )
    search_results_per_page = models.IntegerField(
        blank=False,
        default=getattr(settings, 'WAGGYLABS_SEARCH_RESULTS_PAGE_SIZE', 10),
        verbose_name=_('Number of search results per page'),
        validators=[
            MinValueValidator(
                1,
                message=_('Number of search results per page '
                          'cannot be less than 1.')
            ),
        ],
    )
    class PaginatorAlignment(models.TextChoices):
        """Width of the main content. Final width depends on the presence of
        the sidebar. See waggylabs_tags.py for width calculation."""
        LEFT = 'justify-content-start', _('Left')
        CENTER = 'justify-content-center', _('Center')
        RIGHT = 'justify-content-end', _('Right')
    paginator_alignment = models.CharField(
        max_length=25,
        choices=PaginatorAlignment.choices,
        default=PaginatorAlignment.CENTER,
        blank=False,
        help_text=_('Sets the paginator alignment on the page.'),
        verbose_name=_('Paginator alignment'),
    )
    class PaginatorSize(models.TextChoices):
        """Width of the main content. Final width depends on the presence of
        the sidebar. See waggylabs_tags.py for width calculation."""
        NORMAL = '', _('Normal')
        SMALL = 'pagination-sm', _('Small')
        LARGE = 'pagination-lg', _('Large')
    paginator_size = models.CharField(
        max_length=15,
        blank=True,
        choices=PaginatorSize.choices,
        default=PaginatorSize.NORMAL,
        help_text=_('Sets the paginator text and icon size.'),
        verbose_name=_('Paginator size'),
    )
    first_page_text = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Text for the first button text.'),
        verbose_name=_('First page button text'),
    )
    first_page_icon = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Icon for the first button text.'),
        verbose_name=_('First page button icon'),
    )
    previous_page_text =  models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Text for the previous button text.'),
        verbose_name=_('Previous page button text'),
    )
    previous_page_icon = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Icon for the previous button text.'),
        verbose_name=_('Previous page button icon'),
    )
    next_page_text = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Text for the next button text.'),
        verbose_name=_('Next page button text'),
    )
    next_page_icon = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Icon for the next button text.'),
        verbose_name=_('Next page button icon'),
    )
    last_page_text = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Text for the last button text.'),
        verbose_name=_('Last page button text'),
    )
    last_page_icon = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Icon for the last button text.'),
        verbose_name=_('Last page button icon'),
    )

    # Panels for the Wagtail admin
    site_name_panels = [
        HelpPanel(content=_('Site brand settings include icon, '
                            'site name, optional slogan, and their '
                            'alignment settings.'),
                  heading=_('Explanation of the settings'),
                  classname='title'),
        FieldPanel('site_icon'),
        FieldPanel('site_slogan'),
        FieldPanel('show_site_name'),
        FieldPanel('site_name_separator'),
        FieldPanel('site_name_alignment'),
    ]
    
    content_panels = [
        HelpPanel(content=_('Content settings regulate the general appearance '
                            'of the site. They include the custom Bootstrap CSS theme, '
                            'if this theme supports color modes, and the width of the '
                            'page content.'),
                  heading=_('Explanation of the settings'),
                  classname='title'),
        FieldPanel('site_theme'),
        FieldPanel('theme_supports_color_mode'),
        FieldPanel('content_width'),
        FieldPanel('constant_content_width'),
    ]
    
    navbar_panels = [
        HelpPanel(content=_('Navigation bar settings define the color of the '
                            'navigation bar, its color mode, menu location, additional '
                            'links e.g. to social media accounts.'
                            'Select the correct navigation bar theme especially if '
                            'custom CSS file was used. Select the desired placement of the '
                            'navigation bar and the alignment of the menu links.'),
                  heading=_('Explanation of the settings'),
                  classname='title'),
        # FieldPanel('navbar_theme'),
        FieldPanel('navbar_color', widget=ColorInput),
        FieldPanel('navbar_link_color', widget=ColorInput),
        FieldPanel('navbar_hover_link_color', widget=ColorInput),
        FieldPanel('navbar_link_weight'),
        FieldPanel('navbar_active_link_color', widget=ColorInput),
        FieldPanel('navbar_active_link_weight'),
        FieldPanel('navbar_placement'),
        FieldPanel('navbar_menu_alignment'),
        FieldPanel('navbar_links'),
    ]
    
    footer_panels = [
        HelpPanel(content=_('Footer settings include content lisencing information '
                            'and general content located in the footer, such as '
                            'duplicating navigation bar menu, block with external '
                            'and/or internal links, and blocks related to posts in '
                            'the blog.'),
                  heading=_('Explanation of the settings'),
                  classname='title'),
        MultiFieldPanel([
            FieldPanel('copyright_icon', widget=IconInput),
            FieldPanel('copyright_info'),
            FieldPanel('content_license_link'),
            FieldPanel('content_license_text'),
        ], heading=_('Content license settings')),
        FieldPanel('footer'),
    ]
    
    search_panels = [
        HelpPanel(content=_('Search settings govern the presence of the search '
                            'button in the menu and the appearance of the search '
                            'results on the page. Paginator settings determine the '
                            'look of the navigation buttons on the page.'),
                  heading=_('Explanation of the settings'),
                  classname='title'),
        FieldPanel('search_in_menu'),
        FieldPanel('search_results_per_page'),
        MultiFieldPanel([
            FieldPanel('paginator_alignment'),
            FieldPanel('paginator_size'),
            FieldPanel('first_page_text'),
            FieldPanel('first_page_icon', widget=IconInput),
            FieldPanel('previous_page_text'),
            FieldPanel('previous_page_icon', widget=IconInput),
            FieldPanel('next_page_text'),
            FieldPanel('next_page_icon', widget=IconInput),
            FieldPanel('last_page_text'),
            FieldPanel('last_page_icon', widget=IconInput),
        ], heading=_('Paginator settings')),
    ]
    
    edit_handler = TabbedInterface([
        ObjectList(site_name_panels, heading=_('Site name settings')),
        ObjectList(navbar_panels, heading=_('Navigation bar settings')),
        ObjectList(content_panels, heading=_('Content settings')),
        ObjectList(footer_panels, heading=_('Footer settings')),
        ObjectList(search_panels, heading=_('Search settings')),
    ])
    
    class Meta:
        verbose_name = _('Waggy Labs Settings')