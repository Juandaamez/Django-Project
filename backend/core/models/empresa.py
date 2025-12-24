from django.db import models

class Empresa(models.Model):
    nit = models.CharField(
        max_length=20,
        primary_key=True
    )
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre
