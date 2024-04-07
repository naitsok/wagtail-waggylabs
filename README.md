[![PyPI](https://img.shields.io/badge/PyPI-v1.1.0-orange)](https://pypi.org/project/wagtail-waggylabs/)
[![License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)

# Wagtail-Waggylabs 1.1.0

Waggylabs 1.1.0 was updated to use Wagtail 6 and it was not tested with Wagtail 5.2. For use with Wagtail 5.2, use Waggylabs 1.0.x.

WaggyLabs is a [Django](https://docs.djangoproject.com/) and [Wagtail CMS](https://wagtail.org/>) app for scientific blogs and research group websites. Check the [demo page](https://ktamarov.com/waggylabs-demo) to see most of the features.


## Features

1. Complex complex pages for publishing scientific article-like posts and beyond. The pages include various comonents such as with different elements including figures, tables, code, image carousels, etc. Check the demo page at 

2. LaTeX equations are supported out of the box. The Markdown editor is extended with LaTeX equation and autocomplete.

3. Referencing figures, tables, code listings, etc. made easy! Just use the standard LaTeX syntax \\ref{...} in the Markdown text fields. Autocomplete lists available identifiers.

4. Adding literature is simplified. Add the literature block enywhere and reference it in the text with LaTeX \\cite{...} command. Autocomplete helps to track the available literature identifiers.

5. Custom Bootstrap themes can be used with or without the dark/bright modes.

6. All the Bootsrap component are supported including e.g. image carousels, accordions, collapses, etc.

7. Lots of custom page components such as sidebar, sidebar tabs, page visuals, page content, tag cloud, categories list, post archive, menus, footer, etc.

8. Finally, WaggyLabs comes with all the Wagtail features for administering puslishing process. Check Wagtail's [User Guide](https://guide.wagtail.org/en-latest/)!

## Installation

WaggyLabs should be installed as a typical Django app into the existing Django project. An example of such project can be found on the [WaggyLabs GitHub](https://github.com/naitsok/wagtail-waggylabs>) page. It is good to have basic understanting of [Wagtail CMS](https://wagtail.org/) and its configuration. Tested with latest Wagtail version.

Installation steps:

1. `pip install wagtail-waggylabs`

2. Make sure that the `INSALLED_APPS` variable in the `settings.base.py` contains the following apps

    ```python
    INSTALLED_APPS = [
        "waggylabs",
        
        "wagtail.contrib.forms",
        # "wagtail.contrib.modeladmin",
        "wagtail.contrib.redirects",
        "wagtail.contrib.routable_page",
        "wagtail.contrib.settings",
        "wagtail.contrib.styleguide",
        "wagtail.contrib.table_block",
        "wagtail.embeds",
        "wagtail.sites",
        "wagtail.users",
        "wagtail.snippets",
        "wagtail.documents",
        "wagtail.images",
        "wagtail.search",
        "wagtail.admin",
        "wagtail",
        
        "modelcluster",
        "taggit",
        # "taggit_templatetags",
        "el_pagination",
        "wagtailmenus",
        "wagtailmarkdown",
        "wagtailmetadata",
        "hitcount",
        "captcha",
        
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.sitemaps",
        
        # Other apps for the project
    ]
    ```

3. If needed, add `waggylabs.middleware.DjangoAdminAccessMiddleware` to the `MIDDLEWARE`. This middleware prevents opening `/django-admin/` if a user has not logged in through `Wagtail` login page.

4. Add `wagtail.contrib.settings.context_processors.settings` and `wagtailmenus.context_processors.wagtailmenus` to the `context_processors` list of `TEMPLATES`.

5. Configure `wagtailmarkdown`
   
    ```pyhton
    WAGTAILMARKDOWN = {
        # ...
        "allowed_tags": ["s"],
        "extensions": [
            "waggylabs.extensions.markdown",
            ],
        "extension_configs": {
            "codehilite": {
                "linenums": True,
                }
            },
        "extensions_settings_mode": "extend",
    }
    ```

6. Configure [django-simple-captcha](https://guide.wagtail.org/en-latest/) if you intend to use it. For example,

    ```python
    CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
    # CAPTCHA_IMAGE_SIZE = (120, 60)
    CAPTCHA_FONT_SIZE = 30
    ```

7. Include the WaggyLabs URLconf into your Django project

    ```python
    from wagtail import urls as wagtail_urls
    from waggylabs import urls as waggylabs_urls
    urlpatterns = [
        path("", include(waggylabs_urls)),
    ]
    if settings.DEBUG:
        from django.conf.urls.static import static
        from django.contrib.staticfiles.urls import staticfiles_urlpatterns

        # Serve static and media files from development server
        urlpatterns += staticfiles_urlpatterns()
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = urlpatterns + [
        # For anything not caught by a more specific rule above, hand over to
        # Wagtail's page serving mechanism. This should be the last pattern in
        # the list:
        path("", include(wagtail_urls)),
        # Alternatively, if you want Wagtail pages to be served from a subpath
        # of your site, rather than the site root:
        #    path("pages/", include(wagtail_urls)),
    ]
    ```

8. In order to properly initiazlie the django-hitcount with the demo homepage, the following set of commands in this order

    ```python
    python manage.py migrate
    python manage.py makemigrations
    python manage.py migrate
    ```

9.  Run `python manage.py createsuperuser` to be able to login to Wagtail admin.

10.  Start the development server `python manage.py runserver` and navigate to http://127.0.0.1:8000/ or similar shown url in your browser to see the demo page. If you have configured `WAGGYLABS_BASE_URL`, then the demo page will appear at the http://127.0.0.1:8000/WAGGYLABS_BASE_URL/ url. To login to Wagtail admin, go to the http://127.0.0.1:8000/WAGGYLABS_BASE_URL/WAGGYLABS_WAGTAIL_ADMIN_BASE_URL/ url.

## Settings

There are few additional setting for the WaggyLabs in addition to the settings of the different packages used.

1. Settings related to the url configuration

    ```python
    # WAGGYLABS_BASE_URL sets the base url for the whole WaggyLabs site
    # i.e. the total url will be WAGGYLABS_BASE_URL + all other parts
    # (For example, Django admin base url will be WAGGYLABS_BASE_URL +
    # WAGGYLABS_DJANGO_ADMIN_BASE_URL). This is needed when a WaggyLabs
    # site is added to an existing Django project.
    WAGGYLABS_BASE_URL = ''
    WAGGYLABS_DJANGO_ADMIN_BASE_URL = 'django-admin/'
    WAGGYLABS_WAGTAIL_ADMIN_BASE_URL = 'admin/'
    WAGGYLABS_WAGTAIL_DOCUMENTS_BASE_URL = 'documents/'
    WAGGYLABS_CAPTCHA_BASE_URL = 'super-captcha/'
    WAGGYLABS_SEARCH_URL = 'search/'
    ```

2. Settings to control menu generated by [wagtailmenus](https://wagtailmenus.readthedocs.io/en/stable/) in addition to `wagtailmenus` settings

    ```python
    # Sets the default value for the main menu sublevels in the WaggyLabs site settings admin page. The value can be changed in the admin page.
    WAGGYLABS_MENU_MAX_LEVELS = 1
    # Controls the appearance of the menu item when its submenu opens. Again, this is the default value for the WaggyLabs site settings admin page and can be changed there
    WAGGYLABS_MENU_ALLOW_REPEATING_PARENTS = True
    ```

3. Settings for various blocks

    ```python
    # Maximum number of columns in the card grid block
    WAGGYLABS_CARD_GRID_COLUMNS = 3
    # Codemirror modes for the code block
    # The dictionary entry has the following structure
    # 'CodeMirror MIME type': ('CodeMirror mode folder', 'Pygments short name', 'Human readable name')
    WAGGYLABS_CODEBLOCK_LANGS =  {
        # 'CodeMirror MIME type': ('CodeMirror mode folder', 'Pygments short name', 'Human readable name')
        # https://codemirror.net/5/mode/index.html
        # https://pygments.org/languages/
        'text/x-python': ('python', 'python', 'Python'),
        'text/x-csrc': ('clike', 'c', 'C'),
        'text/x-c++src': ('clike', 'cpp', 'C++'),
        'text/x-java': ('clike', 'java', 'Java/Kotlin'),
        'text/x-csharp': ('clike', 'csharp', 'C#'),
        'text/x-objectivec': ('clike', 'objectivec', 'Objective C'),
        'text/x-scala': ('clike', 'scala', 'Scala'),
        # 'text/x-django': ('django', 'django', 'Django template markup'), # Not working
        # 'text/x-dockerfile': ('dockerfile', 'dockerfile', 'Dockerfile'),  # Not working
        'application/xml': ('xml', 'xml', 'XML'), # Needs to be before HTML mode
        'text/html': ('htmlmixed', 'html', 'HTML'),
        'text/javascript': ('javascript', 'javascript', 'Javascipt'),
        'text/json': ('javascript', 'json', 'JSON'),
        'text/typescript': ('javascript', 'typescript', 'TypeScript'),
        'text/x-mathematica': ('mathematica', 'mathematica', 'Mathematica'),
        'text/x-octave': ('octave', 'matlab', 'Matlab'),
        'application/x-powershell': ('powershell', 'powershell', 'Powershell'),
        # 'text/x-rsrc': ('r', 'r', 'R'),
        # 'text/x-rustsrc': ('rust', 'rust', 'Rust'),  # Not working
        'text/x-sh': ('shell', 'bach', 'Bach/Shell'),
        'text/x-swift': ('swift', 'swift', 'Swift'),
        'text/x-sql': ('sql', 'sql', 'SQL'),
    }
    # Maximum number of columns in the columns block
    WAGGYLABS_COLUMNS_MAX = 3
    ```

### Important settings of the packages

The following list shows the important settings of different packages used in WaggyLabs.

1. `django-hitcount` settings

    ```python
    # after this time the hit from the same user will be counted again
    HITCOUNT_KEEP_HIT_ACTIVE  = { "days" : 30 }
    ```

2. `django-el-pagination` settings

    ```python
    # Function to generate page labels for widget rendering
    EL_PAGINATION_PAGE_LIST_CALLABLE = 'el_pagination.utils.get_elastic_page_numbers' # get_page_numbers
    ```

3. `django-taggit` settings

    ```python
    TAGGIT_CASE_INSENSITIVE = True
    TAG_SPACES_ALLOWED = True
    ```

4. `wagtailmenus` settings

    ```python
    WAGTAILMENUS_ACTIVE_ANCESTOR_CLASS = "active"
    WAGTAILMENUS_SECTION_ROOT_DEPTH = 3
    ```

5. `wagtail` settings

    ```python
    # Wagtail settings
    WAGTAIL_APPEND_SLASH = True
    WAGTAIL_SITE_NAME = "WaggyLabs"

    # Search
    # https://docs.wagtail.org/en/stable/topics/search/backends.html
    WAGTAILSEARCH_BACKENDS = {
        "default": {
            "BACKEND": "wagtail.search.backends.database",
        }
    }

    # Base URL to use when referring to full URLs within the Wagtail admin backend -
    # e.g. in notification emails. Don't include '/admin' or a trailing slash
    WAGTAILADMIN_BASE_URL = "http://example.com"
    # Search backed for development
    WAGTAILSEARCH_BACKENDS = {
        'default': {
            'BACKEND': 'wagtail.search.backends.database',
        }
    }

    # Disable password reset since it is personal site and the user is created using command line
    WAGTAIL_PASSWORD_RESET_ENABLED = True

    # Passwords can be changed
    WAGTAIL_PASSWORD_MANAGEMENT_ENABLED = True

    # Users do have passwords to log in
    WAGTAILUSERS_PASSWORD_ENABLED = True

    # Users must have paswords
    WAGTAILUSERS_PASSWORD_REQUIRED = True

    # See also embeds configuration at https://docs.wagtail.org/en/stable/reference/settings.html#wagtailembeds-responsive-html
    WAGTAILEMBEDS_RESPONSIVE_HTML = True

    # Custom admin login form based on email
    # To have default login form, comment the line
    WAGTAILADMIN_USER_LOGIN_FORM = 'waggylabs.forms.CaptchaLoginForm'

    # Changes whether the Submit for Moderation button is displayed in the action menu
    WAGTAIL_MODERATION_ENABLED = True

    # To count usage of images and documents
    WAGTAIL_USAGE_COUNT_ENABLED = True

    # Date and time formats for admin
    # WAGTAIL_DATE_FORMAT = '%d.%m.%Y.'
    # WAGTAIL_DATETIME_FORMAT = '%d.%m.%Y. %H:%M'
    # WAGTAIL_TIME_FORMAT = '%H:%M'
    ```

## Changelog

### Version 1.1.0

- Updated to Django 5.0.x and Wagtail 6.0.x. Not verified if Waggylabs 1.1.0 works with Wagtial 5.2.x.
- Redone Color widget and Icon chooser widget. New appearance and working with Stimulus.
- Updated Markdown widget to work with stimulus. Improved Markdown widget Javascript code for faster pwerformance (removed the need to trigger all the markdown widgets into preview mode for Mathjax to work correctly).
- Updated Table widget to be in line with Wagtail's Table block. Converting to work together is still pending as in Wagtail 6.
- Updated Wagtail admin login for for Django simple captcha to work with vanilla Javascript and Stimulus.

### Version 1.0.4

- Improved Autocomplete function on EasyMDE editors used in Wagtail admin. Improved MathJax typesetting when previewing Markdown in EasyMDE.

### Version 1.0.3

- Updated Django and Wagtail to 5.0.1 and 5.2.2 versions. Dependent packages has been also updated.

### Version 1.0.2

- Changed the migrations in order to show well-composed demo page after migraitions applied for the first time.
- Added badges to the README.md

### Version 1.0.1

- Minor bugfixes in Link blocks to correctly display buttons and links.

### Version 1.0

WaggyLabs package and WaggyLabs site are ready and can be launched on a DigitalOcean droplet via Docker containers.

### Version 1.0b1

Initial release with the main features presented in the "Features" section on top of the page.

## Future plans

1. [Stimulus](https://stimulus.hotwired.dev/) for the frontend.
2. Comments for posts.