"""
Configuración de la App Django para el Dominio
"""
from django.apps import AppConfig


class LitethinkingDomainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'litethinking_domain'
    verbose_name = 'Dominio - Lite Thinking'
