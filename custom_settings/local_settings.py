import os


# This must point to the Tangra directory on your server
ROOT_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), os.path.pardir))


# The place to serve static files from. STATIC_ROOT is where collectstatic dumps them from
#STATIC_URL = 'http://tangra.ruralbuiltenvironment.com/static/'
#STATIC_ROOT = '/srv/www/static/'

#STATIC_URL = os.path.normpath(os.path.join(ROOT_PATH, "static")) + "/"
STATIC_URL = "/static/"
STATICFILES_DIRS = (
    os.path.normpath(os.path.join(ROOT_PATH, "static")) + "/",
)


# This is the directory where Tangra will store all user generated/uploaded files
USER_FILES = os.path.join(ROOT_PATH, "media/user_files/")

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4=ic*0&yk7rh@zyxbrq*-+&i9tqj16j%m4@0sbwe%plxw(%%3b'

# Database customization
# DATABASE_NAME = os.path.join(ROOT_PATH, 'db/portal.db')             # Or path to database file if using sqlite3.
# DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
# DATABASE_USER = ''             # Not used with sqlite3.
# DATABASE_PASSWORD = ''         # Not used with sqlite3.
# DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
# DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT_PATH, 'db/portal.db'),
    }
}

ADMINS = (
    ('Dr. D', 'dr_d@dr_d.com'),
)