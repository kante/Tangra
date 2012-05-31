import os
# point this to the Tangra directory on your server

ROOT_PATH = '/Users/kante/Documents/work/tangra/Tangra'


# The place to serve static files from
#STATIC_URL = 'http://192.168.74.136'
#STATIC_ROOT = '/Library/WebServer/Documents/media/'
#STATICFILES_DIRS = (
#    ROOT_PATH + "/media/",
#)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4=ic*0&yk7rh@zyxbrq*-+&i9tqj16j%m4@0sbwe%plxw(%%3b'

# Database customization
DATABASE_NAME = os.path.join(ROOT_PATH, 'db/portal.db')             # Or path to database file if using sqlite3.
DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


# ???
LOCKDOWN_PASSWORD = ('jetta')
