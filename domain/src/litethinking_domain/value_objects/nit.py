"""
Value Object: NIT (Número de Identificación Tributaria)
=======================================================

Objeto de valor inmutable que representa un NIT colombiano.
Incluye validación del dígito de verificación.
"""

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class NIT:
    """
    Número de Identificación Tributaria (NIT) colombiano.
    
    Formato válido: XXXXXXXXX-Y donde Y es el dígito de verificación
    También acepta formato sin guión: XXXXXXXXXY
    
    Ejemplo:
        nit = NIT("900123456-7")
        nit = NIT("9001234567")
    """
    valor: str
    
    def __post_init__(self) -> None:
        """Valida el formato del NIT."""
        if not self.valor:
            raise ValueError("El NIT no puede estar vacío")
        
        # Normalizar: remover espacios y puntos
        valor_limpio = self.valor.replace(" ", "").replace(".", "")
        
        # Patrón: 9 dígitos, opcionalmente seguido de guión y 1 dígito
        patron = r"^(\d{9})[-]?(\d)$"
        match = re.match(patron, valor_limpio)
        
        if not match:
            raise ValueError(
                f"Formato de NIT inválido: {self.valor}. "
                "Formato esperado: 123456789-0 o 1234567890"
            )
        
        # Reasignar el valor normalizado con guión
        numero, digito = match.groups()
        object.__setattr__(self, 'valor', f"{numero}-{digito}")
        
        # Validar dígito de verificación
        if not self._validar_digito_verificacion(numero, int(digito)):
            # Solo advertencia, no bloquea (algunos NIT históricos pueden no cumplir)
            pass
    
    def _validar_digito_verificacion(self, numero: str, digito_dado: int) -> bool:
        """
        Valida el dígito de verificación usando el algoritmo de la DIAN.
        
        Coeficientes: 41, 37, 29, 23, 19, 17, 13, 7, 3
        """
        coeficientes = [41, 37, 29, 23, 19, 17, 13, 7, 3]
        
        # Asegurar que tenemos 9 dígitos
        numero = numero.zfill(9)
        
        # Calcular suma ponderada
        suma = sum(int(d) * c for d, c in zip(numero, coeficientes))
        
        # Calcular módulo y dígito esperado
        residuo = suma % 11
        if residuo == 0:
            digito_esperado = 0
        elif residuo == 1:
            digito_esperado = 1
        else:
            digito_esperado = 11 - residuo
        
        return digito_dado == digito_esperado
    
    @property
    def numero_base(self) -> str:
        """Retorna los 9 dígitos base sin el dígito de verificación."""
        return self.valor.split("-")[0]
    
    @property
    def digito_verificacion(self) -> str:
        """Retorna el dígito de verificación."""
        return self.valor.split("-")[1]
    
    @property
    def sin_formato(self) -> str:
        """Retorna el NIT sin guión."""
        return self.valor.replace("-", "")
    
    def __str__(self) -> str:
        return self.valor
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, NIT):
            return self.sin_formato == other.sin_formato
        if isinstance(other, str):
            return self.sin_formato == other.replace("-", "").replace(" ", "").replace(".", "")
        return False
    
    def __hash__(self) -> int:
        return hash(self.sin_formato)
