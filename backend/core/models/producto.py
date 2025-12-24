from django.db import models
from .empresa import Empresa

class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    caracteristicas = models.TextField()
    precios = models.JSONField()
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='productos'
    )

    def __str__(self):
        return self.nombre
