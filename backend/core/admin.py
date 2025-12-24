from django.contrib import admin
from .models import Empresa, Producto, Inventario

admin.site.register(Empresa)
admin.site.register(Producto)
admin.site.register(Inventario)
