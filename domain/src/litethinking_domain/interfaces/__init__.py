"""
Interfaces del Dominio
======================

Contratos (ports) que definen cómo la capa de dominio interactúa
con la infraestructura, sin conocer detalles de implementación.
"""

from litethinking_domain.interfaces.repositories import (
    IEmpresaRepository,
    IProductoRepository,
    IInventarioRepository,
    IHistorialEnvioRepository,
)
from litethinking_domain.interfaces.services import (
    IEmailService,
    IPDFService,
    IIAService,
    IBlockchainService,
)

__all__ = [
    # Repositorios
    "IEmpresaRepository",
    "IProductoRepository",
    "IInventarioRepository",
    "IHistorialEnvioRepository",
    # Servicios
    "IEmailService",
    "IPDFService",
    "IIAService",
    "IBlockchainService",
]
