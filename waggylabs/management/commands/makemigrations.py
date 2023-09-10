from django.apps import apps
from django.core.management.commands.makemigrations import Command as OriginalCommand


IGNORED_MISSING_MIGRATIONS = {
    'hitcount',
    'wagtailmentus',
}


class Command(OriginalCommand):
    """Replate the original 'makemigrations' command to avoid
    creating unnessary migrations for 'hitcount' and 'wagtailmenus' apps.
    """
    def handle(self, *app_labels, **options):
        # if app_labels or not options['check_changes']:
        #     return super().handle(*app_labels, **options)

        app_labels = {cfg.label for cfg in apps.get_app_configs()} - IGNORED_MISSING_MIGRATIONS
        return super().handle(*app_labels, **options)