"""
Tests unitarios para la API REST.
Incluye tests para serializers, views y endpoints.
"""
import json
from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from core.models import Empresa, Producto, Inventario, HistorialEnvio
from .serializers import (
    EmpresaSerializer,
    ProductoSerializer,
    InventarioSerializer,
    HistorialEnvioSerializer,
)

User = get_user_model()


# ═══════════════════════════════════════════════════════════════
# TESTS DE SERIALIZERS
# ═══════════════════════════════════════════════════════════════

class EmpresaSerializerTest(TestCase):
    """Tests para EmpresaSerializer"""
    
    def setUp(self):
        self.empresa_data = {
            'nit': '900123456-1',
            'nombre': 'Empresa Test',
            'direccion': 'Calle 123',
            'telefono': '3001234567'
        }
    
    def test_serializer_con_datos_validos(self):
        """Test: Serializer acepta datos válidos"""
        serializer = EmpresaSerializer(data=self.empresa_data)
        self.assertTrue(serializer.is_valid())
    
    def test_serializer_sin_nit(self):
        """Test: Serializer rechaza datos sin NIT"""
        data = self.empresa_data.copy()
        del data['nit']
        serializer = EmpresaSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('nit', serializer.errors)
    
    def test_serializer_campos_correctos(self):
        """Test: Serializer tiene los campos correctos"""
        empresa = Empresa.objects.create(**self.empresa_data)
        serializer = EmpresaSerializer(empresa)
        self.assertEqual(set(serializer.data.keys()), {'nit', 'nombre', 'direccion', 'telefono'})


class ProductoSerializerTest(TestCase):
    """Tests para ProductoSerializer"""
    
    def setUp(self):
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
            'empresa': self.empresa.nit
        }
    
    def test_serializer_con_datos_validos(self):
        """Test: Serializer acepta datos válidos"""
        serializer = ProductoSerializer(data=self.producto_data)
        self.assertTrue(serializer.is_valid())
    
    def test_serializer_incluye_empresa_nombre(self):
        """Test: Serializer incluye nombre de empresa"""
        producto = Producto.objects.create(
            codigo='PROD-001',
            nombre='Producto Test',
            caracteristicas='Características',
            precios={'COP': 10000},
            empresa=self.empresa
        )
        serializer = ProductoSerializer(producto)
        self.assertEqual(serializer.data['empresa_nombre'], 'Empresa Test')


class InventarioSerializerTest(TestCase):
    """Tests para InventarioSerializer"""
    
    def setUp(self):
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
        self.inventario = Inventario.objects.create(
            producto=self.producto,
            cantidad=100
        )
    
    def test_serializer_campos_relacionados(self):
        """Test: Serializer incluye campos relacionados"""
        serializer = InventarioSerializer(self.inventario)
        self.assertEqual(serializer.data['producto_codigo'], 'PROD-001')
        self.assertEqual(serializer.data['producto_nombre'], 'Producto Test')
        self.assertEqual(serializer.data['producto_empresa'], '900123456-1')
        self.assertEqual(serializer.data['producto_empresa_nombre'], 'Empresa Test')


# ═══════════════════════════════════════════════════════════════
# TESTS DE AUTENTICACIÓN
# ═══════════════════════════════════════════════════════════════

class AuthenticationTest(APITestCase):
    """Tests para autenticación JWT"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.login_url = reverse('auth-login')
    
    def test_login_exitoso(self):
        """Test: Login con credenciales válidas"""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
    
    def test_login_email_incorrecto(self):
        """Test: Login con email incorrecto"""
        data = {
            'email': 'wrong@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_password_incorrecto(self):
        """Test: Login con contraseña incorrecta"""
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_usuario_inactivo(self):
        """Test: Login con usuario inactivo"""
        self.user.is_active = False
        self.user.save()
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ═══════════════════════════════════════════════════════════════
# TESTS DE ENDPOINTS DE EMPRESA
# ═══════════════════════════════════════════════════════════════

class EmpresaAPITest(APITestCase):
    """Tests para endpoints de Empresa"""
    
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.normal_user = User.objects.create_user(
            username='normal',
            email='normal@example.com',
            password='normalpass123'
        )
        self.empresa = Empresa.objects.create(
            nit='900123456-1',
            nombre='Empresa Test',
            direccion='Calle 123',
            telefono='3001234567'
        )
        self.list_url = reverse('empresa-list')
        self.detail_url = reverse('empresa-detail', kwargs={'pk': self.empresa.nit})
    
    def test_listar_empresas_sin_autenticacion(self):
        """Test: Listar empresas sin autenticación (permitido)"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_crear_empresa_sin_autenticacion(self):
        """Test: Crear empresa sin autenticación (denegado)"""
        data = {
            'nit': '900999999-9',
            'nombre': 'Nueva Empresa',
            'direccion': 'Nueva Dirección',
            'telefono': '3009999999'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_crear_empresa_usuario_normal(self):
        """Test: Crear empresa con usuario normal (denegado)"""
        self.client.force_authenticate(user=self.normal_user)
        data = {
            'nit': '900999999-9',
            'nombre': 'Nueva Empresa',
            'direccion': 'Nueva Dirección',
            'telefono': '3009999999'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_crear_empresa_admin(self):
        """Test: Crear empresa con admin (permitido)"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'nit': '900999999-9',
            'nombre': 'Nueva Empresa',
            'direccion': 'Nueva Dirección',
            'telefono': '3009999999'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_obtener_empresa_detalle(self):
        """Test: Obtener detalle de empresa"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Empresa Test')
    
    def test_buscar_empresa_por_nombre(self):
        """Test: Buscar empresa por nombre"""
        response = self.client.get(self.list_url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)


# ═══════════════════════════════════════════════════════════════
# TESTS DE ENDPOINTS DE PRODUCTO
# ═══════════════════════════════════════════════════════════════

class ProductoAPITest(APITestCase):
    """Tests para endpoints de Producto"""
    
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
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
        self.list_url = reverse('producto-list')
        self.detail_url = reverse('producto-detail', kwargs={'pk': self.producto.id})
    
    def test_listar_productos(self):
        """Test: Listar productos"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_filtrar_productos_por_empresa(self):
        """Test: Filtrar productos por empresa"""
        response = self.client.get(self.list_url, {'empresa': self.empresa.nit})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_crear_producto_crea_inventario(self):
        """Test: Crear producto también crea inventario"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'codigo': 'PROD-002',
            'nombre': 'Nuevo Producto',
            'caracteristicas': 'Nuevas características',
            'precios': {'COP': 20000},
            'empresa': self.empresa.nit,
            'cantidad_inicial': 50
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que se creó el inventario
        producto = Producto.objects.get(codigo='PROD-002')
        inventario = Inventario.objects.filter(producto=producto).first()
        self.assertIsNotNone(inventario)
        self.assertEqual(inventario.cantidad, 50)


# ═══════════════════════════════════════════════════════════════
# TESTS DE ENDPOINTS DE INVENTARIO
# ═══════════════════════════════════════════════════════════════

class InventarioAPITest(APITestCase):
    """Tests para endpoints de Inventario"""
    
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
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
        self.inventario = Inventario.objects.create(
            producto=self.producto,
            cantidad=100
        )
        self.list_url = reverse('inventario-list')
        self.detail_url = reverse('inventario-detail', kwargs={'pk': self.inventario.id})
    
    def test_listar_inventario_sin_autenticacion(self):
        """Test: Listar inventario sin autenticación (denegado)"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_listar_inventario_autenticado(self):
        """Test: Listar inventario autenticado"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_filtrar_inventario_por_empresa(self):
        """Test: Filtrar inventario por empresa"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.list_url, {'empresa': self.empresa.nit})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_actualizar_cantidad_inventario(self):
        """Test: Actualizar cantidad de inventario"""
        self.client.force_authenticate(user=self.admin_user)
        data = {'cantidad': 200}
        response = self.client.patch(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.inventario.refresh_from_db()
        self.assertEqual(self.inventario.cantidad, 200)


# ═══════════════════════════════════════════════════════════════
# TESTS DE GENERACIÓN DE PDF
# ═══════════════════════════════════════════════════════════════

class GenerarPDFAPITest(APITestCase):
    """Tests para endpoint de generación de PDF"""
    
    def setUp(self):
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
        self.producto = Producto.objects.create(
            codigo='PROD-001',
            nombre='Producto Test',
            caracteristicas='Características',
            precios={'COP': 10000},
            empresa=self.empresa
        )
        self.inventario = Inventario.objects.create(
            producto=self.producto,
            cantidad=100
        )
        self.pdf_url = reverse('inventario-pdf', kwargs={'empresa_nit': self.empresa.nit})
    
    def test_generar_pdf_sin_autenticacion(self):
        """Test: Generar PDF sin autenticación (denegado)"""
        response = self.client.get(self.pdf_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_generar_pdf_autenticado(self):
        """Test: Generar PDF autenticado"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.pdf_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')
    
    def test_generar_pdf_empresa_no_existe(self):
        """Test: Generar PDF de empresa que no existe"""
        self.client.force_authenticate(user=self.user)
        url = reverse('inventario-pdf', kwargs={'empresa_nit': 'NO-EXISTE'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# ═══════════════════════════════════════════════════════════════
# TESTS DE ENVÍO DE CORREO
# ═══════════════════════════════════════════════════════════════

class EnviarCorreoAPITest(APITestCase):
    """Tests para endpoint de envío de correo"""
    
    def setUp(self):
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
        self.producto = Producto.objects.create(
            codigo='PROD-001',
            nombre='Producto Test',
            caracteristicas='Características',
            precios={'COP': 10000},
            empresa=self.empresa
        )
        self.inventario = Inventario.objects.create(
            producto=self.producto,
            cantidad=100
        )
        self.correo_url = reverse('inventario-enviar-correo')
    
    def test_enviar_correo_sin_autenticacion(self):
        """Test: Enviar correo sin autenticación (denegado)"""
        data = {
            'empresa_nit': self.empresa.nit,
            'email_destino': 'destino@example.com'
        }
        response = self.client.post(self.correo_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_enviar_correo_sin_empresa_nit(self):
        """Test: Enviar correo sin NIT de empresa"""
        self.client.force_authenticate(user=self.user)
        data = {
            'email_destino': 'destino@example.com'
        }
        response = self.client.post(self.correo_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_enviar_correo_sin_email_destino(self):
        """Test: Enviar correo sin email destino"""
        self.client.force_authenticate(user=self.user)
        data = {
            'empresa_nit': self.empresa.nit
        }
        response = self.client.post(self.correo_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_enviar_correo_empresa_no_existe(self):
        """Test: Enviar correo de empresa que no existe"""
        self.client.force_authenticate(user=self.user)
        data = {
            'empresa_nit': 'NO-EXISTE',
            'email_destino': 'destino@example.com'
        }
        response = self.client.post(self.correo_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    @patch('api.views.enviar_correo_resend')
    def test_enviar_correo_exitoso(self, mock_enviar):
        """Test: Enviar correo exitosamente (mock)"""
        mock_enviar.return_value = {'id': 'test-id-123'}
        self.client.force_authenticate(user=self.user)
        data = {
            'empresa_nit': self.empresa.nit,
            'email_destino': 'destino@example.com',
            'incluir_analisis_ia': False,
            'incluir_blockchain': False
        }
        response = self.client.post(self.correo_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        
        # Verificar que se creó el historial
        historial = HistorialEnvio.objects.filter(empresa=self.empresa).first()
        self.assertIsNotNone(historial)
        self.assertEqual(historial.estado, 'enviado')


# ═══════════════════════════════════════════════════════════════
# TESTS DE HISTORIAL DE ENVÍOS
# ═══════════════════════════════════════════════════════════════

class HistorialEnviosAPITest(APITestCase):
    """Tests para endpoints de historial de envíos"""
    
    def setUp(self):
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
        self.historial = HistorialEnvio.objects.create(
            empresa=self.empresa,
            usuario=self.user,
            email_destino='destino@example.com',
            asunto='Test Subject',
            estado='enviado'
        )
        self.list_url = reverse('historial-envio-list')
    
    def test_listar_historial_sin_autenticacion(self):
        """Test: Listar historial sin autenticación (denegado)"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_listar_historial_autenticado(self):
        """Test: Listar historial autenticado"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_filtrar_historial_por_empresa(self):
        """Test: Filtrar historial por empresa"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url, {'empresa': self.empresa.nit})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)


# ═══════════════════════════════════════════════════════════════
# TESTS DE ANÁLISIS IA
# ═══════════════════════════════════════════════════════════════

class AnalisisIAAPITest(APITestCase):
    """Tests para endpoint de análisis IA"""
    
    def setUp(self):
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
        self.producto = Producto.objects.create(
            codigo='PROD-001',
            nombre='Producto Test',
            caracteristicas='Características',
            precios={'COP': 10000},
            empresa=self.empresa
        )
        self.inventario = Inventario.objects.create(
            producto=self.producto,
            cantidad=100
        )
        self.analisis_url = reverse('inventario-analisis', kwargs={'empresa_nit': self.empresa.nit})
    
    def test_analisis_sin_autenticacion(self):
        """Test: Análisis sin autenticación (denegado)"""
        response = self.client.get(self.analisis_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_analisis_empresa_no_existe(self):
        """Test: Análisis de empresa que no existe"""
        self.client.force_authenticate(user=self.user)
        url = reverse('inventario-analisis', kwargs={'empresa_nit': 'NO-EXISTE'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    @patch('api.views.analizar_inventario')
    def test_analisis_exitoso(self, mock_analizar):
        """Test: Análisis exitoso (mock)"""
        mock_analizar.return_value = {
            'resumen': 'Análisis de prueba',
            'alertas': [],
            'recomendaciones': []
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.analisis_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('analisis', response.data)
