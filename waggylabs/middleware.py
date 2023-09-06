from django.conf import settings
from django.http import Http404


DJANGO_ADMIN_BASE_URL = (getattr(settings, 'WAGGYLABS_DJANGO_ADMIN_BASE_URL', 'django-admin/')
                         .lower().replace(r'^', '').replace(r'/', ''))


class DjangoAdminAccessMiddleware:
    """
    Middleware that provides access for django admin part of the
    website. The access is allowed for users, who first logged into Wagtail admin.
    Others are redirected to 404 page.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if DJANGO_ADMIN_BASE_URL in request.path.lower() and not request.user.is_authenticated:
            # not authenticated users are not allowed to
            # access django admin
            raise Http404

        return self.get_response(request)