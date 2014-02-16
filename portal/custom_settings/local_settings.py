import os

# point this to the Tangra directory on your server
# ROOT_PATH = '/Users/arturomp/Documents/Tareas/TAGlab/tangra'

# point this to the Tangra directory on your server
# ROOT_PATH = 'c:/Users/kante/Desktop/Tangra/'
# more general version, but assumes a specific directory structure
ROOT_PATH = os.path.join(
                        os.path.dirname(__file__), 
                        os.path.pardir, 
                        os.path.pardir
                        )
                        

# The place to serve static files from
STATIC_URL = 'http://tangra.ruralbuiltenvironment.com/static/'
STATIC_ROOT = '/srv/www/static/'
#STATICFILES_DIRS = (
#    ROOT_PATH + "/media/",
#)

# User files
# starts from 'portal' directory
USER_FILES = "../media/user_files/"

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

# ???
LOCKDOWN_PASSWORD = ('jetta')
