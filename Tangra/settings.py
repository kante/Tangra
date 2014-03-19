#Django settings for portal project.
import os
import sys

# Module for non-django settings (cache timeouts, database types, etc...)
from custom_settings import *


sys.path.insert(0, os.path.normpath(os.path.join(ROOT_PATH,".")))
#print >>sys.stderr,  sys.path


DEBUG = True
TEMPLATE_DEBUG = DEBUG
SESSION_COOKIE_AGE = 1209600
ADMINS = (
    ('Dr. D', 'dr_d@dr_d.com'),
)
MANAGERS = ADMINS


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Toronto'

FIXTURE_DIRS = (
    #'../fixtures/'
)


# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
SITE_ID = 1


# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.load_template_source',
    'django.template.loaders.eggs.Loader',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    #'studies.context_processors.msgproc'
)


MIDDLEWARE_CLASSES = (
    # This is used to set up the custom urls.py and views.py in the user_studies
    # app. We will be getting rid of this and have a custom 'build_studies' UI 
    # once the code cleanup is done.
    'Tangra.FileBuilderMiddleware',
    'Tangra.UserActivityMiddleware',
    
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    
    # required for unittesting to work. Can be commented out in a production server.
    'django.contrib.messages.middleware.MessageMiddleware',
)


SESSION_ENGINE = "django.contrib.sessions.backends.db"


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    
    # required for unit testing to work. Can be commented out in a production server
    'django.contrib.messages',
    
    'Tangra.studies',
    # Classes used to extend the basic django User model
    'Tangra.users',
    
    # The basic functionality needed to step through a study. Used by Tangra native and external studies
    'public_api',
    
    # UI and modules for creating user generated studies
    'study_builder',
    
    # User generated studies are dropped in this directory
    'user_studies',
    

    # Libraries
#   'lockdown',

)


# Required for the extension of the django User model
AUTH_PROFILE_MODULE = 'users.UserProfile'



# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
# apparently, this is for user generated content.. TODO: move our static files to STATIC_URL above
MEDIA_ROOT = os.path.normpath(os.path.join(ROOT_PATH, "/media"))

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/amedia/'
#ADMIN_MEDIA_PREFIX = STATIC_URL + "/media/admin/" 

# The location of all html/django templates
TEMPLATE_DIRS = (
	os.path.join(ROOT_PATH, 'Tangra/templates'),
	os.path.join(ROOT_PATH, 'Tangra/templates/study'),
	os.path.join(ROOT_PATH, 'Tangra/templates/study_builder'),
	os.path.join(ROOT_PATH, 'Tangra/templates/investigator'),
)


# Where we store css/js/images
#MEDIA_URL = STATIC_URL + "/media/" 
MEDIA_URL = "/media/"

ROOT_URLCONF = 'Tangra.urls'
