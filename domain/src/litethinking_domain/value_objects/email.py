"""
Value Object: Email
===================

Objeto de valor inmutable que representa una dirección de correo electrónico.
"""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Email:
    """
    Dirección de correo electrónico validada.
    
    Ejemplo:
        email = Email("usuario@ejemplo.com")
    """
    valor: str
    
    # Patrón de validación de email (RFC 5322 simplificado)
    PATRON_EMAIL = re.compile(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )
    
    def __post_init__(self) -> None:
        """Valida el formato del email."""
        if not self.valor:
            raise ValueError("El email no puede estar vacío")
        
        # Normalizar a minúsculas y eliminar espacios
        valor_limpio = self.valor.strip().lower()
        
        if not self.PATRON_EMAIL.match(valor_limpio):
            raise ValueError(f"Formato de email inválido: {self.valor}")
        
        # Reasignar el valor normalizado
        object.__setattr__(self, 'valor', valor_limpio)
    
    @property
    def usuario(self) -> str:
        """Retorna la parte local del email (antes del @)."""
        return self.valor.split("@")[0]
    
    @property
    def dominio(self) -> str:
        """Retorna el dominio del email (después del @)."""
        return self.valor.split("@")[1]
    
    @property
    def es_corporativo(self) -> bool:
        """
        Indica si parece ser un email corporativo.
        (No pertenece a proveedores comunes de email personal)
        """
        dominios_personales = {
            "gmail.com", "hotmail.com", "outlook.com", "yahoo.com",
            "live.com", "icloud.com", "me.com", "mail.com",
            "aol.com", "protonmail.com", "zoho.com"
        }
        return self.dominio not in dominios_personales
    
    def __str__(self) -> str:
        return self.valor
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Email):
            return self.valor == other.valor
        if isinstance(other, str):
            return self.valor == other.strip().lower()
        return False
    
    def __hash__(self) -> int:
        return hash(self.valor)
