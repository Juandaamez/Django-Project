from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from litethinking_domain.entities import Inventario, HistorialEnvio
from litethinking_domain.value_objects import Email, HashBlockchain


@dataclass
class ResultadoEnvioEmail:
    """Resultado de un envío de email."""
    exitoso: bool
    mensaje_id: Optional[str] = None
    proveedor: str = ""
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ResultadoPDF:
    """Resultado de generación de PDF."""
    contenido: bytes
    nombre_archivo: str
    hash: HashBlockchain
    paginas: int = 1


@dataclass
class AnalisisIA:
    """Resultado de análisis de IA."""
    resumen: str
    alertas: List[str]
    recomendaciones: List[str]
    puntuacion_salud: int  # 0-100
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class CertificadoBlockchain:
    """Certificado de registro en blockchain."""
    hash_documento: HashBlockchain
    hash_contenido: HashBlockchain
    timestamp: str
    verificacion_url: str


class IEmailService(ABC):
    
    @abstractmethod
    def enviar(
        self,
        destinatario: Email,
        asunto: str,
        contenido_html: str,
        adjuntos: Optional[List[tuple]] = None
    ) -> ResultadoEnvioEmail:
        """
        Envía un email.
        
        Args:
            destinatario: Email de destino
            asunto: Asunto del correo
            contenido_html: Contenido HTML del correo
            adjuntos: Lista de tuplas (nombre_archivo, bytes_contenido, mime_type)
            
        Returns:
            ResultadoEnvioEmail con el estado del envío
        """
        pass
    
    @abstractmethod
    def enviar_reporte_inventario(
        self,
        destinatario: Email,
        empresa_nombre: str,
        pdf_contenido: bytes,
        resumen: Optional[str] = None
    ) -> ResultadoEnvioEmail:
        """
        Envía un reporte de inventario por email.
        
        Args:
            destinatario: Email de destino
            empresa_nombre: Nombre de la empresa
            pdf_contenido: Contenido del PDF en bytes
            resumen: Resumen opcional del inventario
        """
        pass
    
    @abstractmethod
    def esta_configurado(self) -> bool:
        """Verifica si el servicio está correctamente configurado."""
        pass


class IPDFService(ABC):
    """
    Interfaz del servicio de generación de PDFs.
    
    Define las operaciones para generar documentos PDF.
    """
    
    @abstractmethod
    def generar_reporte_inventario(
        self,
        empresa_nombre: str,
        empresa_nit: str,
        inventarios: List[Dict[str, Any]],
        incluir_analisis_ia: bool = False,
        analisis: Optional[AnalisisIA] = None
    ) -> ResultadoPDF:
        """
        Genera un PDF con el reporte de inventario.
        
        Args:
            empresa_nombre: Nombre de la empresa
            empresa_nit: NIT de la empresa
            inventarios: Lista de items del inventario
            incluir_analisis_ia: Si incluir análisis de IA
            analisis: Análisis de IA opcional
            
        Returns:
            ResultadoPDF con el contenido y metadatos
        """
        pass
    
    @abstractmethod
    def generar_certificado_blockchain(
        self,
        certificado: CertificadoBlockchain,
        empresa_nombre: str
    ) -> ResultadoPDF:
        """
        Genera un PDF con el certificado blockchain.
        
        Args:
            certificado: Datos del certificado
            empresa_nombre: Nombre de la empresa
        """
        pass


class IIAService(ABC):
    """
    Interfaz del servicio de Inteligencia Artificial.
    
    Define las operaciones de análisis con IA.
    """
    
    @abstractmethod
    def analizar_inventario(
        self,
        inventarios: List[Dict[str, Any]],
        historico: Optional[List[Dict[str, Any]]] = None
    ) -> AnalisisIA:
        """
        Analiza el estado del inventario con IA.
        
        Args:
            inventarios: Lista actual del inventario
            historico: Datos históricos opcionales
            
        Returns:
            AnalisisIA con el resultado del análisis
        """
        pass
    
    @abstractmethod
    def generar_prediccion_demanda(
        self,
        producto_codigo: str,
        historico_ventas: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Genera predicción de demanda para un producto.
        
        Args:
            producto_codigo: Código del producto
            historico_ventas: Historial de ventas
        """
        pass
    
    @abstractmethod
    def esta_disponible(self) -> bool:
        """Verifica si el servicio de IA está disponible."""
        pass


class IBlockchainService(ABC):
    """
    Interfaz del servicio de Blockchain.
    
    Define las operaciones de certificación blockchain.
    """
    
    @abstractmethod
    def registrar_documento(
        self,
        contenido: bytes,
        metadata: Dict[str, Any]
    ) -> CertificadoBlockchain:
        """
        Registra un documento en la blockchain.
        
        Args:
            contenido: Bytes del documento
            metadata: Metadatos adicionales
            
        Returns:
            CertificadoBlockchain con la información del registro
        """
        pass
    
    @abstractmethod
    def verificar_documento(
        self,
        hash_documento: HashBlockchain
    ) -> Optional[Dict[str, Any]]:
        """
        Verifica un documento en la blockchain.
        
        Args:
            hash_documento: Hash del documento a verificar
            
        Returns:
            Información del registro si existe, None si no
        """
        pass
    
    @abstractmethod
    def obtener_historial(
        self,
        empresa_nit: str
    ) -> List[Dict[str, Any]]:
        """
        Obtiene el historial de registros blockchain de una empresa.
        
        Args:
            empresa_nit: NIT de la empresa
        """
        pass
