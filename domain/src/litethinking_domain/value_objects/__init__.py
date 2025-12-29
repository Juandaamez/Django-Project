"""
Objetos de Valor del Dominio
============================

Objetos inmutables que representan conceptos del dominio con validaciones propias.
"""

from litethinking_domain.value_objects.nit import NIT
from litethinking_domain.value_objects.email import Email
from litethinking_domain.value_objects.money import Money, Currency
from litethinking_domain.value_objects.hash_blockchain import HashBlockchain
from litethinking_domain.value_objects.codigo_producto import CodigoProducto

__all__ = [
    "NIT",
    "Email",
    "Money",
    "Currency",
    "HashBlockchain",
    "CodigoProducto",
]
