"""
Lite Thinking Domain Layer
==========================

Capa de dominio independiente que contiene las entidades del negocio,
objetos de valor, interfaces y reglas de negocio para el sistema de inventario.

Esta capa sigue los principios de Clean Architecture y está completamente
desacoplada de frameworks, ORMs y detalles de infraestructura.
"""

from litethinking_domain.entities import (
    Empresa,
    Producto,
    Inventario,
    HistorialEnvio,
)
from litethinking_domain.value_objects import (
    NIT,
    Email,
    Money,
    HashBlockchain,
    CodigoProducto,
)

__version__ = "1.0.0"
__author__ = "Lite Thinking Team"

__all__ = [
    # Entidades
    "Empresa",
    "Producto",
    "Inventario",
    "HistorialEnvio",
    # Objetos de Valor
    "NIT",
    "Email",
    "Money",
    "HashBlockchain",
    "CodigoProducto",
]
