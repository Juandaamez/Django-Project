from django.contrib import admin
from litethinking_domain.models import Empresa, Producto, Inventario, HistorialEnvio

admin.site.register(Empresa)
admin.site.register(Producto)
admin.site.register(Inventario)
admin.site.register(HistorialEnvio)
