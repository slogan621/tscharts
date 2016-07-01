import os
import sys

sys.path.append('/home/slogan')
sys.path.append('/home/slogan/')
sys.path.append('/home/slogan/ts/tscharts')
sys.path.append('/home/slogan/ts/tscharts/')
sys.path.append('/home/slogan/ts/tscharts/tscharts')
sys.path.append('/home/slogan/ts/tscharts/tscharts/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
