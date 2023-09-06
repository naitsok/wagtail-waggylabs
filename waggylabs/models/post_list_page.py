from datetime import date, datetime

from django.contrib.auth.models import User
from django.http import Http404
from django.utils.dateformat import DateFormat
from django.utils.formats import date_format
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, re_path
from wagtail.fields import StreamField
from wagtail.search import index

from wagtailmenus.models import MenuPageMixin
from wagtailmenus.panels import menupage_panel

from waggylabs.models.base_page import BasePage
from waggylabs.models.post_category import PostCategory
from waggylabs.blocks.post_list_body import PostListBodyBlock
from waggylabs.models.post_page import PostPage
from waggylabs.models.post_tags import TagProxy


class PostListPage(RoutablePageMixin, BasePage, MenuPageMixin):
    """Post list page handles preview of posts in a list.
    It includes previewing by date, by category, tags, creator, etc."""
    
    # Common fields
    
    page_description = ('This is the main page that rules all the posts and post '
                        'routing. All the post pages are children of the post page. '
                        'Give a good slug name of this page, such as "news" or "blog". '
                        'All the posts then will appear with /news/post-slug url.')
    template = 'waggylabs/pages/post_list_page.html'

    show_in_menus_default = True
    
    # Databse fields
    body = StreamField(
        PostListBodyBlock(),
        use_json_field=True,
        blank=True,
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
    subpage_types = ['waggylabs.PostPage']
    
    # Methods
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['slug'].help_text = _(
        #     'Give this page a well-recognized slug (news, blog, etc.), since '
        #     'it will be in the url for all the children post pages. For example, '
        #     'the final url will be https://domain.com/news/post-page, if '
        #     '"news" was added as slug. If this page is selected as root page of the '
        #     'site, the slug will be skipped in the url.'
        # )
        self.pinned_posts = PostPage.objects.live().filter(pin_in_list=True)
        self.posts = PostPage.objects.live().filter(pin_in_list=False)
        self.filter_header = None
        self.filter_term = None
        
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update({
            'pinned_posts': self.pinned_posts,
            'posts': self.posts,
            'filter_header': self.filter_header,
            'filter_term': self.filter_term,
        })
        return context
        
    @re_path(r'^(\d{4})/(\d{2})/(\d{2})/(.+)/$')
    @re_path(r'^(\d{4})/(jan?|feb?|mar?|apr?|may?|jun?|jul?|aug?|sep?|oct?|nov?|dec?)/(\d{2})/(.+)/$')
    def post_by_slug(self, request, year, month, date, slug, *args, **kwargs):
        """This path serves rendering of PostPage with the slug in the url."""
        post = PostPage.objects.live().filter(slug=slug).first()
        if post:
            return post.serve(request, *args, **kwargs)
        raise Http404
    
    @re_path(r'^(\d{4})/$')
    @re_path(r'^(\d{4})/(\d{2})/$')
    @re_path(r'^(\d{4})/(jan?|feb?|mar?|apr?|may?|jun?|jul?|aug?|sep?|oct?|nov?|dec?)/$')
    @re_path(r'^(\d{4})/(\d{2})/(\d{2})/$')
    @re_path(r'^(\d{4})/(jan?|feb?|mar?|apr?|may?|jun?|jul?|aug?|sep?|oct?|nov?|dec?)/(\d{2})/$')
    def posts_by_date(self, request, year, month=None, day=None, *args, **kwargs):
        """The PostPages are listed by date. No pinned posts after date select."""
        self.pinned_posts = None
        self.posts = PostPage.objects.live().filter(first_published_at__year=year)
        self.filter_header = _('Filtered by appeared at:')
        self.filter_term = year
        if month:
            try:
                month = datetime.strptime(month, '%b').month
            except ValueError:
                month = int(month)
                
            self.posts = self.posts.filter(first_published_at__month=month)
            try:
                df = DateFormat(date(int(year), int(month), 1))
            except ValueError:
                # the year, or month or date is wrong, return 404
                raise Http404(_('Wrong date.'))
            self.filter_term = df.format('F Y')

        if day:
            self.posts = self.posts.filter(first_published_at__day=day)
            self.filter_term = date_format(date(int(year), int(month), int(day)))

        self.posts = self.posts.order_by('-first_published_at')
        return self.serve(request, *args, **kwargs)
    
    @re_path(r'^category/(?P<category>[-\w]+)/$')
    def posts_by_category(self, request, category, *args, **kwargs):
        """The PostPages are listed by tag. No pinned posts after tag select."""
        self.pinned_posts = None
        self.posts = PostPage.objects.live().filter(post_categories__post_category__slug=category).order_by('-first_published_at')
        self.filter_header = _('Posts in category:')
        self.filter_term = PostCategory.objects.get(slug=category).name

        return self.serve(request, *args, **kwargs)
    
    @re_path(r'^tag/(?P<tag>[-\w]+)/$')
    def posts_by_tag(self, request, tag, *args, **kwargs):
        """The PostPages are listed by tag. No pinned posts after tag select."""
        self.pinned_posts = None
        self.posts = PostPage.objects.live().filter(tags__slug=tag).order_by('-first_published_at')
        self.filter_header = _('Filtered by tag:')
        self.filter_term = TagProxy.objects.get(slug=tag).name

        return self.serve(request, *args, **kwargs)
    
    @re_path(r'^by/(?P<username>[-_\w\@\+\.]+)/$')
    def posts_by_owner(self, request, username, *args, **kwargs):
        """The posts listed by owner username."""
        self.pinned_posts = None
        self.posts = PostPage.objects.live().filter(owner__username=username).order_by('-first_published_at')
        self.filter_header = _('Posts published by:')
        owner = User.objects.filter(username=username).first()
        if owner:
            self.filter_term = owner.get_username()
        else:
            self.filter_term = username

        return self.serve(request, *args, **kwargs)

    # @re_path(r'^search/$')
    # def post_search(self, request, *args, **kwargs):
    #     """Handles the search queries for post pages."""
    #     search_query = request.GET.get('q', None)
    #     if search_query:
    #         self.posts = PostPage.objects.live().search(search_query)
    #         self.search_header = _('Search results for:')
    #         self.search_term = search_query

    #         # Log the query so Wagtail can suggest promoted results
    #         Query.get(search_query).add_hit()
        
    #     return self.serve(request, *args, **kwargs)