from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.documents import urls as wagtaildocs_urls


from waggylabs import views as waggylabs_views


DJANGO_ADMIN_BASE_URL =  getattr(settings, 'WAGGYLABS_DJANGO_ADMIN_BASE_URL', 'django-admin/')
WAGTAIL_ADMIN_BASE_URL =  getattr(settings, 'WAGGYLABS_WAGTAIL_ADMIN_BASE_URL', 'admin/')
WAGTAIL_DOCUMENTS_BASE_URL =  getattr(settings, 'WAGGYLABS_WAGTAIL_DOCUMENTS_BASE_URL', 'documents/')
CAPTCHA_BASE_URL = getattr(settings, 'WAGGYLABS_CAPTCHA_BASE_URL', 'captcha/')
SEARCH_URL = getattr(settings, 'WAGGYLABS_SEARCH_URL', 'search/')


urlpatterns = [
    path(DJANGO_ADMIN_BASE_URL, admin.site.urls),
    path(WAGTAIL_ADMIN_BASE_URL, include(wagtailadmin_urls)),
    path(WAGTAIL_DOCUMENTS_BASE_URL, include(wagtaildocs_urls)),
    path(SEARCH_URL, waggylabs_views.search, name="search"),
    # according to django-simple-captcha docs
    path(CAPTCHA_BASE_URL, include('captcha.urls')),
    path('robots.txt', waggylabs_views.RobotsView.as_view()),
    path('sitemap.xml', sitemap),
]

# For testing purposes
if settings.DEBUG:
    from django.views import defaults as default_views
    urlpatterns = [
        path('404/', default_views.page_not_found, kwargs={'exception': Exception("Page not Found")}),
        path('500/', default_views.server_error),
    ] + urlpatterns