"""
Value Object: CodigoProducto
============================

Objeto de valor inmutable que representa el código único de un producto.
"""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class CodigoProducto:
    """
    Código único de identificación de producto.
    
    Formato flexible pero con validaciones:
    - Mínimo 2 caracteres
    - Máximo 50 caracteres
    - Solo alfanuméricos, guiones y guiones bajos
    
    Ejemplo:
        codigo = CodigoProducto("PROD-001")
        codigo = CodigoProducto("SKU_12345")
    """
    valor: str
    
    # Patrón de validación: alfanumérico con guiones y guiones bajos
    PATRON_CODIGO = re.compile(r"^[a-zA-Z0-9\-_]+$")
    
    def __post_init__(self) -> None:
        """Valida el formato del código."""
        if not self.valor:
            raise ValueError("El código del producto no puede estar vacío")
        
        # Normalizar: eliminar espacios y convertir a mayúsculas
        valor_limpio = self.valor.strip().upper()
        
        if len(valor_limpio) < 2:
            raise ValueError("El código debe tener al menos 2 caracteres")
        
        if len(valor_limpio) > 50:
            raise ValueError("El código no puede tener más de 50 caracteres")
        
        if not self.PATRON_CODIGO.match(valor_limpio):
            raise ValueError(
                f"Código inválido: {self.valor}. "
                "Solo se permiten letras, números, guiones (-) y guiones bajos (_)"
            )
        
        object.__setattr__(self, 'valor', valor_limpio)
    
    @property
    def prefijo(self) -> str:
        """
        Extrae el prefijo del código (parte antes del primer guión).
        Útil para categorizar productos.
        """
        if "-" in self.valor:
            return self.valor.split("-")[0]
        if "_" in self.valor:
            return self.valor.split("_")[0]
        return self.valor
    
    @property
    def es_secuencial(self) -> bool:
        """
        Indica si el código parece ser secuencial (termina en números).
        """
        # Obtener la última parte después del último guión
        partes = re.split(r"[-_]", self.valor)
        return partes[-1].isdigit()
    
    def __str__(self) -> str:
        return self.valor
    
    def __repr__(self) -> str:
        return f"CodigoProducto('{self.valor}')"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, CodigoProducto):
            return self.valor == other.valor
        if isinstance(other, str):
            return self.valor == other.strip().upper()
        return False
    
    def __hash__(self) -> int:
        return hash(self.valor)
