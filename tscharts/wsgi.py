"""
sys.path.append('/home/tscharts')
sys.path.append('/home/tscharts/')
sys.path.append('/home/tscharts/ts/tscharts')
sys.path.append('/home/tscharts/ts/tscharts/')
sys.path.append('/home/tscharts/ts/tscharts/tscharts')
sys.path.append('/home/tscharts/ts/tscharts/tscharts/')
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tscharts.settings')

application = get_wsgi_application()
