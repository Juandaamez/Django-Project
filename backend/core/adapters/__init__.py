"""
Adaptadores de Infraestructura
==============================

Este módulo contiene los adaptadores que implementan las interfaces
definidas en la capa de dominio, conectándolas con la infraestructura
de Django (ORM, servicios externos, etc.).

Arquitectura:
- Los adaptadores implementan las interfaces del dominio
- Traducen entre entidades de dominio y modelos Django
- Manejan la persistencia y servicios externos
"""

from core.adapters.repositories import (
    DjangoEmpresaRepository,
    DjangoProductoRepository,
    DjangoInventarioRepository,
    DjangoHistorialEnvioRepository,
)
from core.adapters.mappers import (
    EmpresaMapper,
    ProductoMapper,
    InventarioMapper,
    HistorialEnvioMapper,
)

__all__ = [
    # Repositorios
    "DjangoEmpresaRepository",
    "DjangoProductoRepository",
    "DjangoInventarioRepository",
    "DjangoHistorialEnvioRepository",
    # Mappers
    "EmpresaMapper",
    "ProductoMapper",
    "InventarioMapper",
    "HistorialEnvioMapper",
]
