"""
Modelo Inventario
=================

Representa el stock de un producto en el inventario.
"""
from django.db import models
from litethinking_domain.models.producto import Producto


class Inventario(models.Model):
    """
    Entidad Inventario del dominio.
    
    Atributos:
        producto: Producto asociado
        cantidad: Cantidad en stock
        fecha_actualizacion: Última actualización
    """
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name='inventarios',
        help_text='Producto en inventario'
    )
    cantidad = models.PositiveIntegerField(
        default=0,
        help_text='Cantidad disponible en stock'
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        help_text='Fecha de última actualización'
    )

    class Meta:
        db_table = 'core_inventario'  # Usar tabla existente
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        ordering = ['-fecha_actualizacion']

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} unidades"
    
    @property
    def esta_agotado(self):
        """Indica si el producto está agotado."""
        return self.cantidad == 0
    
    @property
    def stock_bajo(self):
        """Indica si el stock está bajo (menos de 10 unidades)."""
        return self.cantidad < 10
