PROJECT_APPS = ('django_any',)
INSTALLED_APPS = ( 'django.contrib.auth',
                   'django.contrib.contenttypes',
                   'django.contrib.sessions',
                   'django.contrib.sites',
                   'django.contrib.admin',
                   'django_hudson',) + PROJECT_APPS
DATABASE_ENGINE = 'sqlite3'
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.load_template_source',
)
ROOT_URLCONF = 'tests.test_runner'


if __name__ == "__main__":
    import sys, test_runner as settings
    from django.core.management import execute_manager
    if len(sys.argv) == 1:
            sys.argv += ['test'] + list(PROJECT_APPS)
    execute_manager(settings)
