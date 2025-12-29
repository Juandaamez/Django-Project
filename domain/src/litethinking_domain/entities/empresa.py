"""
Entidad Empresa
===============

Representa una empresa en el sistema de inventario.
El NIT es la llave primaria natural del negocio.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from litethinking_domain.value_objects.nit import NIT


@dataclass
class Empresa:
    """
    Entidad de dominio que representa una Empresa.
    
    Atributos:
        nit: Número de Identificación Tributaria (llave primaria)
        nombre: Nombre comercial de la empresa
        direccion: Dirección física
        telefono: Número de contacto
        fecha_creacion: Fecha de registro en el sistema
        activa: Indica si la empresa está activa
    """
    nit: NIT
    nombre: str
    direccion: str
    telefono: str
    fecha_creacion: datetime = field(default_factory=datetime.now)
    activa: bool = True
    
    def __post_init__(self) -> None:
        """Validaciones al crear la entidad."""
        if not self.nombre or len(self.nombre.strip()) < 2:
            raise ValueError("El nombre de la empresa debe tener al menos 2 caracteres")
        if not self.direccion or len(self.direccion.strip()) < 5:
            raise ValueError("La dirección debe tener al menos 5 caracteres")
        if not self.telefono or len(self.telefono.strip()) < 7:
            raise ValueError("El teléfono debe tener al menos 7 caracteres")
        
        # Normalizar valores
        self.nombre = self.nombre.strip()
        self.direccion = self.direccion.strip()
        self.telefono = self.telefono.strip()
    
    def actualizar_datos(
        self,
        nombre: Optional[str] = None,
        direccion: Optional[str] = None,
        telefono: Optional[str] = None
    ) -> "Empresa":
        """
        Crea una nueva instancia con los datos actualizados.
        
        Las entidades son inmutables por defecto para mantener
        la integridad del dominio.
        """
        return Empresa(
            nit=self.nit,
            nombre=nombre or self.nombre,
            direccion=direccion or self.direccion,
            telefono=telefono or self.telefono,
            fecha_creacion=self.fecha_creacion,
            activa=self.activa
        )
    
    def desactivar(self) -> "Empresa":
        """Desactiva la empresa (soft delete)."""
        return Empresa(
            nit=self.nit,
            nombre=self.nombre,
            direccion=self.direccion,
            telefono=self.telefono,
            fecha_creacion=self.fecha_creacion,
            activa=False
        )
    
    def activar(self) -> "Empresa":
        """Reactiva una empresa desactivada."""
        return Empresa(
            nit=self.nit,
            nombre=self.nombre,
            direccion=self.direccion,
            telefono=self.telefono,
            fecha_creacion=self.fecha_creacion,
            activa=True
        )
    
    def __str__(self) -> str:
        return f"{self.nombre} (NIT: {self.nit})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Empresa):
            return False
        return self.nit == other.nit
    
    def __hash__(self) -> int:
        return hash(self.nit)
