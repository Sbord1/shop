import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_shop.settings')

# Inizializza Django
application = get_wsgi_application()

# Importa e esegui create_manager() solo dopo che Django è completamente caricato
from accounts.views import create_manager
create_manager()






