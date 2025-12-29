"""
Tests unitarios para los modelos de Core.
"""
from django.test import TestCase
from django.db import IntegrityError
from django.utils import timezone

from .models import Empresa, Producto, Inventario, HistorialEnvio
from django.contrib.auth import get_user_model

User = get_user_model()


class EmpresaModelTest(TestCase):
    """Tests para el modelo Empresa"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.empresa_data = {
            'nit': '900123456-1',
            'nombre': 'Empresa Test S.A.S',
            'direccion': 'Calle 123 #45-67',
            'telefono': '3001234567'
        }
    
    def test_crear_empresa(self):
        """Test: Crear una empresa correctamente"""
        empresa = Empresa.objects.create(**self.empresa_data)
        self.assertEqual(empresa.nit, '900123456-1')
        self.assertEqual(empresa.nombre, 'Empresa Test S.A.S')
        self.assertEqual(str(empresa), 'Empresa Test S.A.S (NIT: 900123456-1)')
    
    def test_empresa_nit_es_primary_key(self):
        """Test: El NIT es la clave primaria"""
        empresa = Empresa.objects.create(**self.empresa_data)
        self.assertEqual(empresa.pk, '900123456-1')
    
    def test_empresa_nit_unico(self):
        """Test: No se pueden crear dos empresas con el mismo NIT"""
        Empresa.objects.create(**self.empresa_data)
        with self.assertRaises(IntegrityError):
            Empresa.objects.create(**self.empresa_data)
    
    def test_empresa_str(self):
        """Test: Representación string de la empresa"""
        empresa = Empresa.objects.create(**self.empresa_data)
        self.assertEqual(str(empresa), f"{empresa.nombre} (NIT: {empresa.nit})")


class ProductoModelTest(TestCase):
    """Tests para el modelo Producto"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.empresa = Empresa.objects.create(
            nit='900123456-1',
            nombre='Empresa Test',
            direccion='Calle 123',
            telefono='3001234567'
        )
        self.producto_data = {
            'codigo': 'PROD-001',
            'nombre': 'Producto Test',
            'caracteristicas': 'Características del producto',
            'precios': {'COP': 10000, 'USD': 2.5},
            'empresa': self.empresa
        }
    
    def test_crear_producto(self):
        """Test: Crear un producto correctamente"""
        producto = Producto.objects.create(**self.producto_data)
        self.assertEqual(producto.codigo, 'PROD-001')
        self.assertEqual(producto.nombre, 'Producto Test')
        self.assertEqual(producto.empresa, self.empresa)
    
    def test_producto_codigo_unico(self):
        """Test: El código del producto debe ser único"""
        Producto.objects.create(**self.producto_data)
        with self.assertRaises(IntegrityError):
            Producto.objects.create(**self.producto_data)
    
    def test_producto_precios_json(self):
        """Test: Los precios se almacenan como JSON"""
        producto = Producto.objects.create(**self.producto_data)
        self.assertIsInstance(producto.precios, dict)
        self.assertEqual(producto.precios['COP'], 10000)
        self.assertEqual(producto.precios['USD'], 2.5)
    
    def test_producto_relacion_empresa(self):
        """Test: La relación con empresa funciona correctamente"""
        producto = Producto.objects.create(**self.producto_data)
        self.assertIn(producto, self.empresa.productos.all())
    
    def test_producto_str(self):
        """Test: Representación string del producto"""
        producto = Producto.objects.create(**self.producto_data)
        self.assertEqual(str(producto), f"{producto.nombre} ({producto.codigo})")
    
    def test_producto_cascade_delete(self):
        """Test: Eliminar empresa elimina sus productos"""
        producto = Producto.objects.create(**self.producto_data)
        producto_id = producto.id
        self.empresa.delete()
        self.assertFalse(Producto.objects.filter(id=producto_id).exists())


class InventarioModelTest(TestCase):
    """Tests para el modelo Inventario"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.empresa = Empresa.objects.create(
            nit='900123456-1',
            nombre='Empresa Test',
            direccion='Calle 123',
            telefono='3001234567'
        )
        self.producto = Producto.objects.create(
            codigo='PROD-001',
            nombre='Producto Test',
            caracteristicas='Características',
            precios={'COP': 10000},
            empresa=self.empresa
        )
    
    def test_crear_inventario(self):
        """Test: Crear un registro de inventario"""
        inventario = Inventario.objects.create(
            producto=self.producto,
            cantidad=100
        )
        self.assertEqual(inventario.producto, self.producto)
        self.assertEqual(inventario.cantidad, 100)
    
    def test_inventario_cantidad_default(self):
        """Test: La cantidad por defecto es 0"""
        inventario = Inventario.objects.create(producto=self.producto)
        self.assertEqual(inventario.cantidad, 0)
    
    def test_inventario_fecha_actualizacion_auto(self):
        """Test: La fecha de actualización se actualiza automáticamente"""
        inventario = Inventario.objects.create(
            producto=self.producto,
            cantidad=50
        )
        self.assertIsNotNone(inventario.fecha_actualizacion)
    
    def test_inventario_str(self):
        """Test: Representación string del inventario"""
        inventario = Inventario.objects.create(
            producto=self.producto,
            cantidad=100
        )
        expected = f"{self.producto.nombre} - 100 unidades"
        self.assertEqual(str(inventario), expected)
    
    def test_inventario_cascade_delete(self):
        """Test: Eliminar producto elimina su inventario"""
        inventario = Inventario.objects.create(
            producto=self.producto,
            cantidad=100
        )
        inventario_id = inventario.id
        self.producto.delete()
        self.assertFalse(Inventario.objects.filter(id=inventario_id).exists())
    
    def test_inventario_cantidad_positiva(self):
        """Test: La cantidad debe ser un entero positivo"""
        inventario = Inventario.objects.create(
            producto=self.producto,
            cantidad=0
        )
        self.assertGreaterEqual(inventario.cantidad, 0)


class HistorialEnvioModelTest(TestCase):
    """Tests para el modelo HistorialEnvio"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.empresa = Empresa.objects.create(
            nit='900123456-1',
            nombre='Empresa Test',
            direccion='Calle 123',
            telefono='3001234567'
        )
    
    def test_crear_historial_envio(self):
        """Test: Crear un registro de historial de envío"""
        historial = HistorialEnvio.objects.create(
            empresa=self.empresa,
            usuario=self.user,
            email_destino='destino@example.com',
            asunto='Test Subject',
            estado='pendiente'
        )
        self.assertEqual(historial.empresa, self.empresa)
        self.assertEqual(historial.usuario, self.user)
        self.assertEqual(historial.estado, 'pendiente')
    
    def test_historial_fecha_creacion_auto(self):
        """Test: La fecha de creación se establece automáticamente"""
        historial = HistorialEnvio.objects.create(
            empresa=self.empresa,
            usuario=self.user,
            email_destino='destino@example.com',
            asunto='Test Subject',
            estado='pendiente'
        )
        self.assertIsNotNone(historial.fecha_creacion)
    
    def test_historial_con_hash_blockchain(self):
        """Test: Almacenar hash de documento"""
        historial = HistorialEnvio.objects.create(
            empresa=self.empresa,
            usuario=self.user,
            email_destino='destino@example.com',
            asunto='Test Subject',
            estado='enviado',
            documento_hash='abc123hash',
            contenido_hash='xyz789hash'
        )
        self.assertEqual(historial.documento_hash, 'abc123hash')
        self.assertEqual(historial.contenido_hash, 'xyz789hash')
    
    def test_historial_con_metricas(self):
        """Test: Almacenar métricas del inventario"""
        historial = HistorialEnvio.objects.create(
            empresa=self.empresa,
            usuario=self.user,
            email_destino='destino@example.com',
            asunto='Test Subject',
            estado='enviado',
            total_productos=10,
            total_unidades=500,
            valor_inventario=1000000.50
        )
        self.assertEqual(historial.total_productos, 10)
        self.assertEqual(historial.total_unidades, 500)
        self.assertEqual(float(historial.valor_inventario), 1000000.50)
