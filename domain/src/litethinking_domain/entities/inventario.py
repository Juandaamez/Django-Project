"""
Entidad Inventario
==================

Representa el stock de un producto en el inventario.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from litethinking_domain.value_objects.codigo_producto import CodigoProducto


@dataclass
class Inventario:
    """
    Entidad de dominio que representa el inventario de un producto.
    
    Atributos:
        id: Identificador único del registro de inventario
        producto_codigo: Código del producto
        cantidad: Cantidad en stock
        cantidad_minima: Cantidad mínima antes de alerta
        fecha_actualizacion: Última fecha de actualización
    """
    id: Optional[int]
    producto_codigo: CodigoProducto
    cantidad: int
    cantidad_minima: int = 0
    fecha_actualizacion: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self) -> None:
        """Validaciones al crear la entidad."""
        if self.cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        if self.cantidad_minima < 0:
            raise ValueError("La cantidad mínima no puede ser negativa")
    
    @property
    def requiere_reposicion(self) -> bool:
        """Indica si el inventario está por debajo del mínimo."""
        return self.cantidad <= self.cantidad_minima
    
    @property
    def esta_agotado(self) -> bool:
        """Indica si el inventario está agotado."""
        return self.cantidad == 0
    
    def agregar_stock(self, cantidad: int) -> "Inventario":
        """
        Agrega unidades al inventario.
        
        Args:
            cantidad: Cantidad a agregar (debe ser positiva)
            
        Returns:
            Nueva instancia de Inventario actualizada
        """
        if cantidad <= 0:
            raise ValueError("La cantidad a agregar debe ser positiva")
        
        return Inventario(
            id=self.id,
            producto_codigo=self.producto_codigo,
            cantidad=self.cantidad + cantidad,
            cantidad_minima=self.cantidad_minima,
            fecha_actualizacion=datetime.now()
        )
    
    def reducir_stock(self, cantidad: int) -> "Inventario":
        """
        Reduce unidades del inventario.
        
        Args:
            cantidad: Cantidad a reducir (debe ser positiva)
            
        Returns:
            Nueva instancia de Inventario actualizada
            
        Raises:
            ValueError: Si no hay suficiente stock
        """
        if cantidad <= 0:
            raise ValueError("La cantidad a reducir debe ser positiva")
        if cantidad > self.cantidad:
            raise ValueError(
                f"Stock insuficiente. Disponible: {self.cantidad}, Solicitado: {cantidad}"
            )
        
        return Inventario(
            id=self.id,
            producto_codigo=self.producto_codigo,
            cantidad=self.cantidad - cantidad,
            cantidad_minima=self.cantidad_minima,
            fecha_actualizacion=datetime.now()
        )
    
    def establecer_cantidad_minima(self, cantidad_minima: int) -> "Inventario":
        """Establece la cantidad mínima de alerta."""
        if cantidad_minima < 0:
            raise ValueError("La cantidad mínima no puede ser negativa")
        
        return Inventario(
            id=self.id,
            producto_codigo=self.producto_codigo,
            cantidad=self.cantidad,
            cantidad_minima=cantidad_minima,
            fecha_actualizacion=datetime.now()
        )
    
    def calcular_diferencia(self, cantidad_objetivo: int) -> int:
        """
        Calcula la diferencia entre el stock actual y un objetivo.
        
        Positivo: Hay exceso de stock
        Negativo: Falta stock
        """
        return self.cantidad - cantidad_objetivo
    
    def __str__(self) -> str:
        estado = "⚠️ BAJO" if self.requiere_reposicion else "✅ OK"
        return f"Inventario {self.producto_codigo}: {self.cantidad} unidades [{estado}]"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Inventario):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)
