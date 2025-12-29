"""
Modelo Empresa
==============

Representa una empresa en el sistema de inventario.
El NIT es la llave primaria natural del negocio.
"""
from django.db import models


class Empresa(models.Model):
    """
    Entidad Empresa del dominio.
    
    Atributos:
        nit: Número de Identificación Tributaria (llave primaria)
        nombre: Nombre comercial de la empresa
        direccion: Dirección física
        telefono: Número de contacto
    """
    nit = models.CharField(
        max_length=20,
        primary_key=True,
        help_text='Número de Identificación Tributaria'
    )
    nombre = models.CharField(
        max_length=150,
        help_text='Nombre de la empresa'
    )
    direccion = models.CharField(
        max_length=255,
        help_text='Dirección física'
    )
    telefono = models.CharField(
        max_length=20,
        help_text='Teléfono de contacto'
    )

    class Meta:
        db_table = 'core_empresa'  # Usar tabla existente
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} (NIT: {self.nit})"
