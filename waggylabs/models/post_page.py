from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from modelcluster.fields import ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager

from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import StreamField
from wagtail.search import index

from waggylabs.blocks.post_body import PostBodyBlock
from waggylabs.models.base_page import BasePage


WAGGYLABS_BASE_URL = getattr(settings, 'WAGGYLABS_BASE_URL', '')

class PostPage(BasePage):
    """Post page keeps posts content, such as blog posts or
    news posts. It has series functionality to combine posts
    within series of topic-related posts."""
    
    page_description = ('Post page keeps posts content, such as blog posts or '
                        'news posts. It has series functionality to combine posts '
                        'within series of topic-related posts.')
    template = 'waggylabs/pages/base_page.html'
    
    # Common fields
    show_in_menus_default = False
    
    # Database fields
    body = StreamField(
        PostBodyBlock(),
        use_json_field=True,
        blank=True,
    )
    pin_in_list = models.BooleanField(
        default=False,
        help_text=_('Indicates if the post is pinned on the post list page.'),
        verbose_name=_('Pin in list'),
    )
    categories = ParentalManyToManyField(
        'waggylabs.PostCategory',
        verbose_name=_('Categories'),
        blank=True,
    )
    tags = ClusterTaggableManager(
        through='waggylabs.PostPageTag',
        help_text=None,
        blank=True,
    )
    
    # Search index configuration

    search_fields = BasePage.search_fields + [
        index.SearchField('body', partial_match=True, boost=2),
        index.AutocompleteField('body', boost=2),
        index.FilterField('pin_in_list'),
        index.FilterField('categories'),
        index.FilterField('tags'),
    ]
    
    # Editor panels configuration
    
    content_panels = BasePage.content_panels + [
        FieldPanel('body'),
    ]
    promote_panels = BasePage.promote_panels + [
        FieldPanel('tags'),
        InlinePanel('post_categories', label=_('Categories'))
    ]
    settings_panels = BasePage.settings_panels
    
    # Parent page / subpage type rules
    
    parent_page_types = ['waggylabs.PostListPage', 'waggylabs.PostPage']
    subpage_types = ['waggylabs.PostPage']
    
    # Methods
    
    @classmethod
    def can_create_at(cls, parent):
        """If the specific class of the parent page is PostPage,
        the hierarchy of the newly added post will be:
        PostPage -> PostPage -> new PostPage. This is too deep
        heararchy. Series of posts allows only one time ancestor
        for a PostPage in series."""
        if parent.get_parent().specific_class == PostPage:
            return False
        return super().can_create_at(parent)
    
    @classmethod
    def can_exist_under(cls, parent):
        """Same as PostPage.can_creat_at(parent) classmethod."""
        if parent.get_parent().specific_class == PostPage:
            return False
        return super().can_exist_under(parent)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.post_list_page = None
        ancestors = self.get_ancestors(inclusive=False)
        for parent in ancestors:
            # comparing as string is necessary to avoid circular imports
            if parent.specific_class.__name__ == 'PostListPage':
                self.post_list_page = parent.specific
                break
        
    
    def can_move_to(self, parent):
        """Same as PostPage.can_creat_at(parent) classmethod."""
        if parent.get_parent().specific_class == PostPage:
            return False
        return super().can_move_to(parent)
    
    def get_url_parts(self, request=None):
        """Adds date before slug into the path to avoid collisions."""
        if self.live and self.post_list_page:
            (site_id, site_root_url, page_path) = self.post_list_page.get_url_parts(request)
            return (
                site_id,
                site_root_url,
                page_path + self.post_list_page.reverse_subpage(
                    'post_by_slug',
                    args=(
                        self.first_published_at.year,
                        self.first_published_at.strftime('%b').lower(),
                        self.first_published_at.strftime('%d'),
                        self.slug,
                    ),
                )
            )
        return None # (site_id, site_root_url, page_path)
    
    def is_series(self):
        """Verifies that post is in the series of topic-related posts."""
        # parent_page = self.get_parent().specific
        if self.get_parent().specific_class == PostPage:
            # this is the child post of series
            return True
        if self.get_children_count() > 0:
            # this is parent post of series
            return True
        return False
    
    def post_series(self):
        """Gets post series for the current post."""
        parent = self.get_parent()
        if parent.specific_class == PostPage:
            return parent.get_descendants(inclusive=True).live().order_by('first_published_at')
        if self.get_children_count() > 0:
            return self.get_descendants(inclusive=True).live().order_by('first_published_at')
        return []
    
    def sibling_posts(self):
        """Returns previous and next posts for the current post.
        Previous means either previously (chronologically) published or 
        previous post from the series. Next means either (chronologically) 
        published next or next post from the series."""
        series = self.post_series()
        if series:
            series_len = series.count()
            for idx, post in enumerate(series):
                if self.pk == post.pk:
                    if idx == 0:
                        return {
                            'previous_post': PostPage.objects.live().filter(
                                    first_published_at__lt=self.first_published_at
                                ).order_by('-first_published_at').first(),
                            'next_post': series[idx + 1],
                        }
                    if idx == series_len - 1:
                        return {
                            'previous_post': series[idx - 1],
                            'next_post': PostPage.objects.live().filter(
                                    first_published_at__gt=self.first_published_at
                                ).order_by('first_published_at').first(),
                        }
                    return {
                        'previous_post': series[idx - 1],
                        'next_post': series[idx + 1],
                    }
        return {
            'previous_post': PostPage.objects.live().filter(
                    first_published_at__lt=self.first_published_at
                ).order_by('-first_published_at').first(),
            'next_post': PostPage.objects.live().filter(
                    first_published_at__gt=self.first_published_at
                ).order_by('first_published_at').first(),
        }
        
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update(self.sibling_posts())
        context.update({
            'post_list_page': self.post_list_page,
        })
        return context