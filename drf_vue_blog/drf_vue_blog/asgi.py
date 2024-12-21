import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_vue_blog.settings')

application = get_asgi_application()
