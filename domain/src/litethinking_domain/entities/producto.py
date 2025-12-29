"""
Entidad Producto
================

Representa un producto del catálogo de una empresa.
Incluye soporte para precios en múltiples monedas.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional

from litethinking_domain.value_objects.nit import NIT
from litethinking_domain.value_objects.money import Money
from litethinking_domain.value_objects.codigo_producto import CodigoProducto


@dataclass
class Producto:
    """
    Entidad de dominio que representa un Producto.
    
    Atributos:
        codigo: Código único del producto
        nombre: Nombre del producto
        caracteristicas: Descripción y características
        precios: Diccionario de precios por moneda (ej: {"COP": Money, "USD": Money})
        empresa_nit: NIT de la empresa propietaria
        fecha_creacion: Fecha de registro
        activo: Indica si el producto está activo
    """
    codigo: CodigoProducto
    nombre: str
    caracteristicas: str
    precios: Dict[str, Money]
    empresa_nit: NIT
    fecha_creacion: datetime = field(default_factory=datetime.now)
    activo: bool = True
    
    def __post_init__(self) -> None:
        """Validaciones al crear la entidad."""
        if not self.nombre or len(self.nombre.strip()) < 2:
            raise ValueError("El nombre del producto debe tener al menos 2 caracteres")
        if not self.precios:
            raise ValueError("El producto debe tener al menos un precio definido")
        
        # Validar que todos los precios sean positivos
        for moneda, precio in self.precios.items():
            if precio.monto <= 0:
                raise ValueError(f"El precio en {moneda} debe ser mayor a 0")
        
        # Normalizar valores
        self.nombre = self.nombre.strip()
        self.caracteristicas = self.caracteristicas.strip() if self.caracteristicas else ""
    
    def obtener_precio(self, moneda: str) -> Optional[Money]:
        """Obtiene el precio en una moneda específica."""
        return self.precios.get(moneda.upper())
    
    def precio_principal(self) -> Money:
        """
        Retorna el precio principal (COP tiene prioridad, 
        si no existe, retorna el primero disponible).
        """
        if "COP" in self.precios:
            return self.precios["COP"]
        return next(iter(self.precios.values()))
    
    def agregar_precio(self, moneda: str, precio: Money) -> "Producto":
        """Agrega o actualiza un precio en una moneda específica."""
        nuevos_precios = {**self.precios, moneda.upper(): precio}
        return Producto(
            codigo=self.codigo,
            nombre=self.nombre,
            caracteristicas=self.caracteristicas,
            precios=nuevos_precios,
            empresa_nit=self.empresa_nit,
            fecha_creacion=self.fecha_creacion,
            activo=self.activo
        )
    
    def actualizar_datos(
        self,
        nombre: Optional[str] = None,
        caracteristicas: Optional[str] = None,
        precios: Optional[Dict[str, Money]] = None
    ) -> "Producto":
        """Crea una nueva instancia con los datos actualizados."""
        return Producto(
            codigo=self.codigo,
            nombre=nombre or self.nombre,
            caracteristicas=caracteristicas if caracteristicas is not None else self.caracteristicas,
            precios=precios or self.precios,
            empresa_nit=self.empresa_nit,
            fecha_creacion=self.fecha_creacion,
            activo=self.activo
        )
    
    def desactivar(self) -> "Producto":
        """Desactiva el producto (soft delete)."""
        return Producto(
            codigo=self.codigo,
            nombre=self.nombre,
            caracteristicas=self.caracteristicas,
            precios=self.precios,
            empresa_nit=self.empresa_nit,
            fecha_creacion=self.fecha_creacion,
            activo=False
        )
    
    def __str__(self) -> str:
        precio = self.precio_principal()
        return f"{self.nombre} ({self.codigo}) - {precio}"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Producto):
            return False
        return self.codigo == other.codigo
    
    def __hash__(self) -> int:
        return hash(self.codigo)
