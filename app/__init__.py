from __future__ import absolute_import, unicode_literals

# Isso garante que o app Celery seja importado com o Django
from .celery import app as celery_app

__all__ = ("celery_app",)
