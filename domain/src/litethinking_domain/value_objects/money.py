"""
Value Object: Money (Dinero)
============================

Objeto de valor inmutable que representa una cantidad monetaria.
Soporta múltiples monedas y operaciones aritméticas seguras.
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Union


class Currency(Enum):
    """Monedas soportadas por el sistema."""
    COP = "COP"  # Peso Colombiano
    USD = "USD"  # Dólar Estadounidense
    EUR = "EUR"  # Euro
    MXN = "MXN"  # Peso Mexicano
    BRL = "BRL"  # Real Brasileño
    
    @property
    def simbolo(self) -> str:
        """Retorna el símbolo de la moneda."""
        simbolos = {
            "COP": "$",
            "USD": "US$",
            "EUR": "€",
            "MXN": "MX$",
            "BRL": "R$"
        }
        return simbolos.get(self.value, self.value)
    
    @property
    def decimales(self) -> int:
        """Retorna la cantidad de decimales estándar."""
        # COP generalmente no usa decimales en precios al consumidor
        if self == Currency.COP:
            return 0
        return 2


@dataclass(frozen=True)
class Money:
    """
    Representa una cantidad monetaria con su moneda.
    
    Utiliza Decimal para cálculos precisos y evitar errores
    de punto flotante.
    
    Ejemplo:
        precio = Money(1500000, "COP")
        precio_usd = Money(350.50, Currency.USD)
    """
    monto: Decimal
    moneda: Currency
    
    def __init__(self, monto: Union[int, float, Decimal, str], moneda: Union[str, Currency]) -> None:
        """
        Inicializa el objeto Money.
        
        Args:
            monto: Cantidad monetaria (puede ser int, float, Decimal o string)
            moneda: Código de moneda (str o Currency enum)
        """
        # Convertir monto a Decimal
        if isinstance(monto, float):
            # Convertir float a string primero para evitar errores de precisión
            monto_decimal = Decimal(str(monto))
        else:
            monto_decimal = Decimal(monto)
        
        # Convertir moneda a enum
        if isinstance(moneda, str):
            try:
                moneda_enum = Currency(moneda.upper())
            except ValueError:
                raise ValueError(f"Moneda no soportada: {moneda}")
        else:
            moneda_enum = moneda
        
        # Validar monto
        if monto_decimal < 0:
            raise ValueError("El monto no puede ser negativo")
        
        # Redondear al número correcto de decimales
        decimales = moneda_enum.decimales
        monto_redondeado = monto_decimal.quantize(
            Decimal(10) ** -decimales, 
            rounding=ROUND_HALF_UP
        )
        
        object.__setattr__(self, 'monto', monto_redondeado)
        object.__setattr__(self, 'moneda', moneda_enum)
    
    def __add__(self, other: "Money") -> "Money":
        """Suma dos cantidades de la misma moneda."""
        if not isinstance(other, Money):
            raise TypeError("Solo se puede sumar con otro objeto Money")
        if self.moneda != other.moneda:
            raise ValueError(f"No se pueden sumar monedas diferentes: {self.moneda} + {other.moneda}")
        return Money(self.monto + other.monto, self.moneda)
    
    def __sub__(self, other: "Money") -> "Money":
        """Resta dos cantidades de la misma moneda."""
        if not isinstance(other, Money):
            raise TypeError("Solo se puede restar con otro objeto Money")
        if self.moneda != other.moneda:
            raise ValueError(f"No se pueden restar monedas diferentes: {self.moneda} - {other.moneda}")
        resultado = self.monto - other.monto
        if resultado < 0:
            raise ValueError("El resultado no puede ser negativo")
        return Money(resultado, self.moneda)
    
    def __mul__(self, factor: Union[int, float, Decimal]) -> "Money":
        """Multiplica la cantidad por un factor."""
        if isinstance(factor, Money):
            raise TypeError("No se puede multiplicar por otro objeto Money")
        return Money(self.monto * Decimal(str(factor)), self.moneda)
    
    def __truediv__(self, divisor: Union[int, float, Decimal]) -> "Money":
        """Divide la cantidad por un divisor."""
        if isinstance(divisor, Money):
            raise TypeError("No se puede dividir por otro objeto Money")
        if divisor == 0:
            raise ValueError("No se puede dividir por cero")
        return Money(self.monto / Decimal(str(divisor)), self.moneda)
    
    def __lt__(self, other: "Money") -> bool:
        """Compara si es menor que otro Money."""
        if not isinstance(other, Money):
            return NotImplemented
        if self.moneda != other.moneda:
            raise ValueError("No se pueden comparar monedas diferentes")
        return self.monto < other.monto
    
    def __le__(self, other: "Money") -> bool:
        """Compara si es menor o igual que otro Money."""
        if not isinstance(other, Money):
            return NotImplemented
        if self.moneda != other.moneda:
            raise ValueError("No se pueden comparar monedas diferentes")
        return self.monto <= other.monto
    
    def __gt__(self, other: "Money") -> bool:
        """Compara si es mayor que otro Money."""
        if not isinstance(other, Money):
            return NotImplemented
        if self.moneda != other.moneda:
            raise ValueError("No se pueden comparar monedas diferentes")
        return self.monto > other.monto
    
    def __ge__(self, other: "Money") -> bool:
        """Compara si es mayor o igual que otro Money."""
        if not isinstance(other, Money):
            return NotImplemented
        if self.moneda != other.moneda:
            raise ValueError("No se pueden comparar monedas diferentes")
        return self.monto >= other.monto
    
    @classmethod
    def cero(cls, moneda: Union[str, Currency]) -> "Money":
        """Crea un Money con monto cero."""
        return cls(0, moneda)
    
    def es_cero(self) -> bool:
        """Indica si el monto es cero."""
        return self.monto == Decimal(0)
    
    def formato(self, con_simbolo: bool = True, separador_miles: str = ",") -> str:
        """
        Formatea el monto para visualización.
        
        Args:
            con_simbolo: Incluir símbolo de moneda
            separador_miles: Caracter para separar miles
        """
        # Formatear número con separador de miles
        if self.moneda.decimales == 0:
            numero = f"{int(self.monto):,}".replace(",", separador_miles)
        else:
            numero = f"{self.monto:,.{self.moneda.decimales}f}".replace(",", separador_miles)
        
        if con_simbolo:
            return f"{self.moneda.simbolo} {numero}"
        return numero
    
    def to_dict(self) -> dict:
        """Convierte a diccionario para serialización."""
        return {
            "monto": str(self.monto),
            "moneda": self.moneda.value
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Money":
        """Crea un Money desde un diccionario."""
        return cls(data["monto"], data["moneda"])
    
    def __str__(self) -> str:
        return self.formato()
    
    def __repr__(self) -> str:
        return f"Money({self.monto}, {self.moneda.value})"
