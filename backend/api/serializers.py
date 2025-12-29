from rest_framework import serializers

from litethinking_domain.models import Empresa, Producto, Inventario, HistorialEnvio


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = [
            'nit',
            'nombre',
            'direccion',
            'telefono',
        ]


class ProductoSerializer(serializers.ModelSerializer):
    empresa_nombre = serializers.CharField(
        source='empresa.nombre',
        read_only=True
    )

    class Meta:
        model = Producto
        fields = [
            'id',
            'codigo',
            'nombre',
            'caracteristicas',
            'precios',
            'empresa',
            'empresa_nombre',
        ]


class InventarioSerializer(serializers.ModelSerializer):
    producto_codigo = serializers.CharField(
        source='producto.codigo',
        read_only=True
    )
    producto_nombre = serializers.CharField(
        source='producto.nombre',
        read_only=True
    )
    producto_empresa = serializers.CharField(
        source='producto.empresa.nit',
        read_only=True
    )
    producto_empresa_nombre = serializers.CharField(
        source='producto.empresa.nombre',
        read_only=True
    )

    class Meta:
        model = Inventario
        fields = [
            'id',
            'producto',
            'producto_codigo',
            'producto_nombre',
            'producto_empresa',
            'producto_empresa_nombre',
            'cantidad',
            'fecha_actualizacion',
        ]
        read_only_fields = ['fecha_actualizacion']


class HistorialEnvioSerializer(serializers.ModelSerializer):
    """
    Serializer para el historial de envíos de inventario.
    Incluye información de blockchain, análisis IA y metadatos.
    """
    empresa_nombre = serializers.CharField(
        source='empresa.nombre',
        read_only=True
    )
    empresa_nit = serializers.CharField(
        source='empresa.nit',
        read_only=True
    )
    usuario_email = serializers.CharField(
        source='usuario.email',
        read_only=True
    )
    usuario_nombre = serializers.SerializerMethodField()
    
    class Meta:
        model = HistorialEnvio
        fields = [
            'id',
            'empresa',
            'empresa_nit',
            'empresa_nombre',
            'usuario',
            'usuario_email',
            'usuario_nombre',
            'email_destino',
            'asunto',
            'estado',
            'proveedor',
            # Blockchain
            'documento_hash',
            'contenido_hash',
            # Métricas
            'total_productos',
            'total_unidades',
            'valor_inventario',
            # IA
            'resumen_ia',
            'alertas_ia',
            # Respuesta
            'respuesta_api',
            'mensaje_error',
            # Timestamps
            'fecha_creacion',
            'fecha_envio',
        ]
        read_only_fields = [
            'id',
            'empresa',
            'empresa_nit',
            'empresa_nombre',
            'usuario',
            'usuario_email',
            'usuario_nombre',
            'email_destino',
            'asunto',
            'estado',
            'proveedor',
            'documento_hash',
            'contenido_hash',
            'total_productos',
            'total_unidades',
            'valor_inventario',
            'resumen_ia',
            'alertas_ia',
            'respuesta_api',
            'mensaje_error',
            'fecha_creacion',
            'fecha_envio',
        ]
    
    def get_usuario_nombre(self, obj):
        if obj.usuario:
            return obj.usuario.get_full_name() or obj.usuario.username
        return None
