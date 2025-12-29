"""
Entidades del Dominio
====================

Contiene las entidades principales del negocio, completamente
desacopladas de cualquier framework o infraestructura.
"""

from litethinking_domain.entities.empresa import Empresa
from litethinking_domain.entities.producto import Producto
from litethinking_domain.entities.inventario import Inventario
from litethinking_domain.entities.historial_envio import HistorialEnvio, EstadoEnvio, ProveedorEmail

__all__ = [
    "Empresa",
    "Producto",
    "Inventario",
    "HistorialEnvio",
    "EstadoEnvio",
    "ProveedorEmail",
]
