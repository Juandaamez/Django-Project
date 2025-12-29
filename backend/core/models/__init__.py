"""
DEPRECADO: Los modelos ahora están en litethinking_domain.models

Este archivo mantiene compatibilidad con imports antiguos.
Por favor, use: from litethinking_domain.models import Empresa, Producto, ...
"""
from litethinking_domain.models import Empresa, Producto, Inventario, HistorialEnvio

__all__ = ['Empresa', 'Producto', 'Inventario', 'HistorialEnvio']
