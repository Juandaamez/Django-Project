from rest_framework import serializers

from core.models import Empresa, Producto, Inventario


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
