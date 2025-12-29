"""
Modelo HistorialEnvio
=====================

Representa el registro de envío de un reporte de inventario por correo.
Incluye certificación blockchain con hash SHA-256.
"""
import hashlib
import json
from django.db import models
from django.contrib.auth.models import User
from litethinking_domain.models.empresa import Empresa


class HistorialEnvio(models.Model):
    """
    Registra cada envío de reporte de inventario por correo.
    Incluye hash blockchain para verificación de autenticidad.
    """
    ESTADO_CHOICES = [
        ('enviado', 'Enviado'),
        ('fallido', 'Fallido'),
        ('pendiente', 'Pendiente'),
    ]
    
    PROVEEDOR_CHOICES = [
        ('resend', 'Resend API'),
        ('django_smtp', 'Django SMTP'),
        ('manual', 'Manual'),
    ]
    
    # Relaciones
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='historial_envios'
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='envios_realizados'
    )
    
    # Datos del envío
    email_destino = models.EmailField()
    asunto = models.CharField(max_length=255)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    proveedor = models.CharField(max_length=20, choices=PROVEEDOR_CHOICES, default='resend')
    
    # Certificación Blockchain
    documento_hash = models.CharField(
        max_length=64,
        help_text='Hash SHA-256 del PDF para verificación de autenticidad'
    )
    contenido_hash = models.CharField(
        max_length=64,
        help_text='Hash SHA-256 del contenido del inventario'
    )
    
    # Metadatos
    total_productos = models.PositiveIntegerField(default=0)
    total_unidades = models.PositiveIntegerField(default=0)
    valor_inventario = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Análisis IA
    resumen_ia = models.TextField(
        blank=True,
        help_text='Resumen generado por IA del estado del inventario'
    )
    alertas_ia = models.JSONField(
        default=list,
        help_text='Lista de alertas generadas por análisis inteligente'
    )
    
    # Respuesta del proveedor
    respuesta_api = models.JSONField(
        default=dict,
        blank=True,
        help_text='Respuesta del servicio de email'
    )
    mensaje_error = models.TextField(blank=True)
    
    # Timestamps
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'core_historialenvio'  # Usar tabla existente
        verbose_name = 'Historial de Envío'
        verbose_name_plural = 'Historial de Envíos'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"{self.empresa.nombre} → {self.email_destino} ({self.estado})"
    
    @property
    def verificacion_url(self):
        """URL para verificar autenticidad del documento"""
        return f"/verificar/{self.documento_hash[:16]}"
    
    @classmethod
    def generar_hash(cls, contenido: bytes) -> str:
        """Genera hash SHA-256 de bytes"""
        return hashlib.sha256(contenido).hexdigest()
    
    @classmethod
    def generar_hash_inventario(cls, inventarios: list) -> str:
        """Genera hash del contenido del inventario para blockchain"""
        # Crear representación canónica del inventario
        datos = []
        for inv in inventarios:
            datos.append({
                'codigo': inv.get('producto_codigo', ''),
                'nombre': inv.get('producto_nombre', ''),
                'cantidad': inv.get('cantidad', 0),
            })
        
        # Ordenar para consistencia
        datos.sort(key=lambda x: x['codigo'])
        
        # Generar hash
        contenido = json.dumps(datos, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(contenido.encode('utf-8')).hexdigest()
