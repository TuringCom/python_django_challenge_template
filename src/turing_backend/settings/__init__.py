import os

exec("from %s import *" % os.environ.get('DJANGO_SETTINGS_MODULE'))
