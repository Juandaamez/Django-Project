"""
Entidad HistorialEnvio
======================

Representa el registro de envío de un reporte de inventario por correo.
Incluye certificación blockchain con hash SHA-256.
"""

from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, List, Dict, Any

from litethinking_domain.value_objects.nit import NIT
from litethinking_domain.value_objects.email import Email
from litethinking_domain.value_objects.hash_blockchain import HashBlockchain


class EstadoEnvio(Enum):
    """Estados posibles del envío."""
    PENDIENTE = "pendiente"
    ENVIADO = "enviado"
    FALLIDO = "fallido"


class ProveedorEmail(Enum):
    """Proveedores de servicio de correo."""
    RESEND = "resend"
    DJANGO_SMTP = "django_smtp"
    MANUAL = "manual"


@dataclass
class HistorialEnvio:
    """
    Entidad de dominio que representa el historial de envío de reportes.
    
    Incluye certificación blockchain mediante hash SHA-256 del documento
    y del contenido para verificación de autenticidad.
    
    Atributos:
        id: Identificador único
        empresa_nit: NIT de la empresa del reporte
        usuario_id: ID del usuario que realizó el envío
        email_destino: Correo electrónico de destino
        asunto: Asunto del correo
        estado: Estado del envío
        proveedor: Proveedor de servicio de email
        documento_hash: Hash SHA-256 del PDF
        contenido_hash: Hash SHA-256 del contenido del inventario
        total_productos: Número de productos en el reporte
        total_unidades: Suma total de unidades
        valor_inventario: Valor monetario total
        resumen_ia: Resumen generado por IA
        alertas_ia: Lista de alertas del análisis inteligente
        respuesta_api: Respuesta del servicio de email
        mensaje_error: Mensaje de error si falló
        fecha_creacion: Fecha de creación del registro
        fecha_envio: Fecha efectiva del envío
    """
    id: Optional[int]
    empresa_nit: NIT
    email_destino: Email
    asunto: str
    documento_hash: HashBlockchain
    contenido_hash: HashBlockchain
    estado: EstadoEnvio = EstadoEnvio.PENDIENTE
    proveedor: ProveedorEmail = ProveedorEmail.RESEND
    usuario_id: Optional[int] = None
    total_productos: int = 0
    total_unidades: int = 0
    valor_inventario: Decimal = field(default_factory=lambda: Decimal("0.00"))
    resumen_ia: str = ""
    alertas_ia: List[str] = field(default_factory=list)
    respuesta_api: Dict[str, Any] = field(default_factory=dict)
    mensaje_error: str = ""
    fecha_creacion: datetime = field(default_factory=datetime.now)
    fecha_envio: Optional[datetime] = None
    
    def __post_init__(self) -> None:
        """Validaciones al crear la entidad."""
        if not self.asunto or len(self.asunto.strip()) < 3:
            raise ValueError("El asunto debe tener al menos 3 caracteres")
        if self.total_productos < 0:
            raise ValueError("El total de productos no puede ser negativo")
        if self.total_unidades < 0:
            raise ValueError("El total de unidades no puede ser negativo")
        if self.valor_inventario < 0:
            raise ValueError("El valor del inventario no puede ser negativo")
        
        self.asunto = self.asunto.strip()
    
    @property
    def verificacion_url(self) -> str:
        """URL para verificar autenticidad del documento."""
        return f"/verificar/{self.documento_hash.valor[:16]}"
    
    @property
    def es_exitoso(self) -> bool:
        """Indica si el envío fue exitoso."""
        return self.estado == EstadoEnvio.ENVIADO
    
    @property
    def tiene_alertas(self) -> bool:
        """Indica si hay alertas de IA."""
        return len(self.alertas_ia) > 0
    
    def marcar_enviado(self) -> "HistorialEnvio":
        """Marca el envío como exitoso."""
        return HistorialEnvio(
            id=self.id,
            empresa_nit=self.empresa_nit,
            email_destino=self.email_destino,
            asunto=self.asunto,
            documento_hash=self.documento_hash,
            contenido_hash=self.contenido_hash,
            estado=EstadoEnvio.ENVIADO,
            proveedor=self.proveedor,
            usuario_id=self.usuario_id,
            total_productos=self.total_productos,
            total_unidades=self.total_unidades,
            valor_inventario=self.valor_inventario,
            resumen_ia=self.resumen_ia,
            alertas_ia=self.alertas_ia,
            respuesta_api=self.respuesta_api,
            mensaje_error=self.mensaje_error,
            fecha_creacion=self.fecha_creacion,
            fecha_envio=datetime.now()
        )
    
    def marcar_fallido(self, error: str, respuesta: Optional[Dict[str, Any]] = None) -> "HistorialEnvio":
        """Marca el envío como fallido."""
        return HistorialEnvio(
            id=self.id,
            empresa_nit=self.empresa_nit,
            email_destino=self.email_destino,
            asunto=self.asunto,
            documento_hash=self.documento_hash,
            contenido_hash=self.contenido_hash,
            estado=EstadoEnvio.FALLIDO,
            proveedor=self.proveedor,
            usuario_id=self.usuario_id,
            total_productos=self.total_productos,
            total_unidades=self.total_unidades,
            valor_inventario=self.valor_inventario,
            resumen_ia=self.resumen_ia,
            alertas_ia=self.alertas_ia,
            respuesta_api=respuesta or self.respuesta_api,
            mensaje_error=error,
            fecha_creacion=self.fecha_creacion,
            fecha_envio=None
        )
    
    def agregar_analisis_ia(self, resumen: str, alertas: List[str]) -> "HistorialEnvio":
        """Agrega el análisis de IA al historial."""
        return HistorialEnvio(
            id=self.id,
            empresa_nit=self.empresa_nit,
            email_destino=self.email_destino,
            asunto=self.asunto,
            documento_hash=self.documento_hash,
            contenido_hash=self.contenido_hash,
            estado=self.estado,
            proveedor=self.proveedor,
            usuario_id=self.usuario_id,
            total_productos=self.total_productos,
            total_unidades=self.total_unidades,
            valor_inventario=self.valor_inventario,
            resumen_ia=resumen,
            alertas_ia=alertas,
            respuesta_api=self.respuesta_api,
            mensaje_error=self.mensaje_error,
            fecha_creacion=self.fecha_creacion,
            fecha_envio=self.fecha_envio
        )
    
    def __str__(self) -> str:
        estado_emoji = {
            EstadoEnvio.PENDIENTE: "⏳",
            EstadoEnvio.ENVIADO: "✅",
            EstadoEnvio.FALLIDO: "❌"
        }
        return f"{estado_emoji[self.estado]} {self.empresa_nit} → {self.email_destino}"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HistorialEnvio):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id) if self.id else hash((self.empresa_nit, self.documento_hash))
