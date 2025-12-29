"""
Modelo Producto
===============

Representa un producto del catálogo de una empresa.
Incluye soporte para precios en múltiples monedas.
"""
from django.db import models
from litethinking_domain.models.empresa import Empresa


class Producto(models.Model):
    """
    Entidad Producto del dominio.
    
    Atributos:
        codigo: Código único del producto
        nombre: Nombre del producto
        caracteristicas: Descripción y características
        precios: Diccionario de precios por moneda (JSONField)
        empresa: Empresa propietaria del producto
    """
    codigo = models.CharField(
        max_length=50,
        unique=True,
        help_text='Código único del producto'
    )
    nombre = models.CharField(
        max_length=150,
        help_text='Nombre del producto'
    )
    caracteristicas = models.TextField(
        blank=True,
        help_text='Características y descripción del producto'
    )
    precios = models.JSONField(
        default=dict,
        help_text='Precios en diferentes monedas: {"COP": 1000, "USD": 0.25}'
    )
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='productos',
        help_text='Empresa propietaria del producto'
    )

    class Meta:
        db_table = 'core_producto'  # Usar tabla existente
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"
    
    def obtener_precio(self, moneda: str = 'COP'):
        """Obtiene el precio en una moneda específica."""
        return self.precios.get(moneda.upper())
