import os
import sys

sys.path.append('/home/tscharts')
sys.path.append('/home/tscharts/')
sys.path.append('/home/tscharts/ts/tscharts')
sys.path.append('/home/tscharts/ts/tscharts/')
sys.path.append('/home/tscharts/ts/tscharts/tscharts')
sys.path.append('/home/tscharts/ts/tscharts/tscharts/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
