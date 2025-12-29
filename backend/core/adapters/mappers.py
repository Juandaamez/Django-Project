"""
Mappers: Traductores entre Entidades de Dominio y Modelos Django
================================================================

Los mappers son responsables de traducir bidireccionalmentee entre:
- Entidades de dominio (puras, sin dependencias de Django)
- Modelos Django (con ORM y dependencias de infraestructura)

Esto mantiene la capa de dominio desacoplada de la infraestructura.
"""

from datetime import datetime
from decimal import Decimal
from typing import Dict, Any, Optional

from django.contrib.auth.models import User

# Importar modelos Django
from core.models import Empresa as EmpresaModel
from core.models import Producto as ProductoModel
from core.models import Inventario as InventarioModel
from core.models import HistorialEnvio as HistorialEnvioModel

# Importar entidades y value objects del dominio
# Nota: Estas importaciones funcionarán cuando el paquete domain esté instalado
try:
    from litethinking_domain.entities import (
        Empresa as EmpresaDomain,
        Producto as ProductoDomain,
        Inventario as InventarioDomain,
        HistorialEnvio as HistorialEnvioDomain,
        EstadoEnvio,
        ProveedorEmail,
    )
    from litethinking_domain.value_objects import (
        NIT, Email, Money, CodigoProducto, HashBlockchain
    )
    DOMAIN_AVAILABLE = True
except ImportError:
    # Fallback si el paquete domain no está instalado
    DOMAIN_AVAILABLE = False


class EmpresaMapper:
    """
    Mapper para la entidad Empresa.
    Traduce entre EmpresaModel (Django) y EmpresaDomain (Dominio).
    """
    
    @staticmethod
    def to_domain(model: EmpresaModel) -> "EmpresaDomain":
        """
        Convierte un modelo Django a entidad de dominio.
        
        Args:
            model: Modelo Django de Empresa
            
        Returns:
            Entidad de dominio Empresa
        """
        if not DOMAIN_AVAILABLE:
            raise ImportError("El paquete litethinking-domain no está instalado")
        
        # Intentar crear NIT validado, o usar string directamente si falla
        try:
            nit = NIT(model.nit)
        except ValueError:
            # NIT legacy no válido, crear uno con padding para compatibilidad
            nit_str = model.nit.zfill(10) if len(model.nit) < 10 else model.nit
            if "-" not in nit_str:
                nit_str = nit_str[:-1] + "-" + nit_str[-1]
            try:
                nit = NIT(nit_str)
            except ValueError:
                # Último recurso: crear un NIT ficticio y usar el original como string
                # Esto permite compatibilidad con datos legacy
                from dataclasses import dataclass
                @dataclass(frozen=True)
                class NITLegacy:
                    valor: str
                    def __str__(self): return self.valor
                    def __eq__(self, other): return str(self) == str(other)
                    def __hash__(self): return hash(self.valor)
                nit = NITLegacy(model.nit)
        
        return EmpresaDomain(
            nit=nit,
            nombre=model.nombre,
            direccion=model.direccion,
            telefono=model.telefono,
            activa=True  # El modelo Django no tiene este campo aún
        )
    
    @staticmethod
    def to_model(entity: "EmpresaDomain") -> EmpresaModel:
        """
        Convierte una entidad de dominio a modelo Django.
        
        Args:
            entity: Entidad de dominio Empresa
            
        Returns:
            Modelo Django de Empresa (no guardado)
        """
        return EmpresaModel(
            nit=str(entity.nit),
            nombre=entity.nombre,
            direccion=entity.direccion,
            telefono=entity.telefono
        )
    
    @staticmethod
    def to_dict(entity: "EmpresaDomain") -> Dict[str, Any]:
        """
        Convierte una entidad de dominio a diccionario.
        Útil para serialización.
        """
        return {
            "nit": str(entity.nit),
            "nombre": entity.nombre,
            "direccion": entity.direccion,
            "telefono": entity.telefono,
            "activa": entity.activa
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "EmpresaDomain":
        """
        Crea una entidad de dominio desde un diccionario.
        Útil para deserialización.
        """
        if not DOMAIN_AVAILABLE:
            raise ImportError("El paquete litethinking-domain no está instalado")
        
        return EmpresaDomain(
            nit=NIT(data["nit"]),
            nombre=data["nombre"],
            direccion=data["direccion"],
            telefono=data["telefono"],
            activa=data.get("activa", True)
        )


class ProductoMapper:
    """
    Mapper para la entidad Producto.
    Traduce entre ProductoModel (Django) y ProductoDomain (Dominio).
    """
    
    @staticmethod
    def to_domain(model: ProductoModel) -> "ProductoDomain":
        """
        Convierte un modelo Django a entidad de dominio.
        """
        if not DOMAIN_AVAILABLE:
            raise ImportError("El paquete litethinking-domain no está instalado")
        
        # Convertir precios JSON a objetos Money
        precios = {}
        if model.precios:
            for moneda, monto in model.precios.items():
                try:
                    precios[moneda.upper()] = Money(monto, moneda)
                except (ValueError, KeyError):
                    continue
        
        return ProductoDomain(
            codigo=CodigoProducto(model.codigo),
            nombre=model.nombre,
            caracteristicas=model.caracteristicas or "",
            precios=precios,
            empresa_nit=NIT(model.empresa.nit),
            activo=True
        )
    
    @staticmethod
    def to_model(entity: "ProductoDomain", empresa_model: EmpresaModel) -> ProductoModel:
        """
        Convierte una entidad de dominio a modelo Django.
        
        Args:
            entity: Entidad de dominio Producto
            empresa_model: Modelo Django de la empresa asociada
        """
        # Convertir objetos Money a JSON serializable
        precios_json = {}
        for moneda, precio in entity.precios.items():
            precios_json[moneda] = float(precio.monto)
        
        return ProductoModel(
            codigo=str(entity.codigo),
            nombre=entity.nombre,
            caracteristicas=entity.caracteristicas,
            precios=precios_json,
            empresa=empresa_model
        )
    
    @staticmethod
    def to_dict(entity: "ProductoDomain") -> Dict[str, Any]:
        """Convierte una entidad de dominio a diccionario."""
        precios_dict = {}
        for moneda, precio in entity.precios.items():
            precios_dict[moneda] = {
                "monto": str(precio.monto),
                "moneda": precio.moneda.value
            }
        
        return {
            "codigo": str(entity.codigo),
            "nombre": entity.nombre,
            "caracteristicas": entity.caracteristicas,
            "precios": precios_dict,
            "empresa_nit": str(entity.empresa_nit),
            "activo": entity.activo
        }


class InventarioMapper:
    """
    Mapper para la entidad Inventario.
    Traduce entre InventarioModel (Django) y InventarioDomain (Dominio).
    """
    
    @staticmethod
    def to_domain(model: InventarioModel) -> "InventarioDomain":
        """Convierte un modelo Django a entidad de dominio."""
        if not DOMAIN_AVAILABLE:
            raise ImportError("El paquete litethinking-domain no está instalado")
        
        return InventarioDomain(
            id=model.id,
            producto_codigo=CodigoProducto(model.producto.codigo),
            cantidad=model.cantidad,
            cantidad_minima=0,  # El modelo Django no tiene este campo aún
            fecha_actualizacion=model.fecha_actualizacion
        )
    
    @staticmethod
    def to_model(entity: "InventarioDomain", producto_model: ProductoModel) -> InventarioModel:
        """Convierte una entidad de dominio a modelo Django."""
        inventario = InventarioModel(
            producto=producto_model,
            cantidad=entity.cantidad
        )
        if entity.id:
            inventario.id = entity.id
        return inventario
    
    @staticmethod
    def to_dict(entity: "InventarioDomain") -> Dict[str, Any]:
        """Convierte una entidad de dominio a diccionario."""
        return {
            "id": entity.id,
            "producto_codigo": str(entity.producto_codigo),
            "cantidad": entity.cantidad,
            "cantidad_minima": entity.cantidad_minima,
            "requiere_reposicion": entity.requiere_reposicion,
            "esta_agotado": entity.esta_agotado
        }


class HistorialEnvioMapper:
    """
    Mapper para la entidad HistorialEnvio.
    """
    
    @staticmethod
    def to_domain(model: HistorialEnvioModel) -> "HistorialEnvioDomain":
        """Convierte un modelo Django a entidad de dominio."""
        if not DOMAIN_AVAILABLE:
            raise ImportError("El paquete litethinking-domain no está instalado")
        
        # Mapear estado
        estado_map = {
            'enviado': EstadoEnvio.ENVIADO,
            'fallido': EstadoEnvio.FALLIDO,
            'pendiente': EstadoEnvio.PENDIENTE,
        }
        estado = estado_map.get(model.estado, EstadoEnvio.PENDIENTE)
        
        # Mapear proveedor
        proveedor_map = {
            'resend': ProveedorEmail.RESEND,
            'django_smtp': ProveedorEmail.DJANGO_SMTP,
            'manual': ProveedorEmail.MANUAL,
        }
        proveedor = proveedor_map.get(model.proveedor, ProveedorEmail.RESEND)
        
        return HistorialEnvioDomain(
            id=model.id,
            empresa_nit=NIT(model.empresa.nit),
            email_destino=Email(model.email_destino),
            asunto=model.asunto,
            documento_hash=HashBlockchain(model.documento_hash) if model.documento_hash else HashBlockchain.desde_texto("placeholder"),
            contenido_hash=HashBlockchain(model.contenido_hash) if model.contenido_hash else HashBlockchain.desde_texto("placeholder"),
            estado=estado,
            proveedor=proveedor,
            usuario_id=model.usuario.id if model.usuario else None,
            total_productos=model.total_productos,
            total_unidades=model.total_unidades,
            valor_inventario=model.valor_inventario,
            resumen_ia=model.resumen_ia or "",
            alertas_ia=model.alertas_ia or [],
            respuesta_api=model.respuesta_api or {},
            mensaje_error=model.mensaje_error or "",
            fecha_creacion=model.fecha_creacion,
            fecha_envio=model.fecha_envio
        )
    
    @staticmethod
    def to_model(
        entity: "HistorialEnvioDomain",
        empresa_model: EmpresaModel,
        usuario: Optional[User] = None
    ) -> HistorialEnvioModel:
        """Convierte una entidad de dominio a modelo Django."""
        
        # Mapear estado inverso
        estado_map = {
            EstadoEnvio.ENVIADO: 'enviado',
            EstadoEnvio.FALLIDO: 'fallido',
            EstadoEnvio.PENDIENTE: 'pendiente',
        }
        
        # Mapear proveedor inverso
        proveedor_map = {
            ProveedorEmail.RESEND: 'resend',
            ProveedorEmail.DJANGO_SMTP: 'django_smtp',
            ProveedorEmail.MANUAL: 'manual',
        }
        
        historial = HistorialEnvioModel(
            empresa=empresa_model,
            usuario=usuario,
            email_destino=str(entity.email_destino),
            asunto=entity.asunto,
            estado=estado_map.get(entity.estado, 'pendiente'),
            proveedor=proveedor_map.get(entity.proveedor, 'resend'),
            documento_hash=str(entity.documento_hash),
            contenido_hash=str(entity.contenido_hash),
            total_productos=entity.total_productos,
            total_unidades=entity.total_unidades,
            valor_inventario=entity.valor_inventario,
            resumen_ia=entity.resumen_ia,
            alertas_ia=entity.alertas_ia,
            respuesta_api=entity.respuesta_api,
            mensaje_error=entity.mensaje_error,
            fecha_envio=entity.fecha_envio
        )
        
        if entity.id:
            historial.id = entity.id
        
        return historial
