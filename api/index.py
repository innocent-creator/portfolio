import os
import sys

# Ajoute la racine du projet au path Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')

from django.core.wsgi import get_wsgi_application
app = get_wsgi_application()
