import hashlib
import os
from unittest.mock import patch, MagicMock

from django.test import TestCase

from .email_service import (
    generar_hash_documento,
    generar_hash_inventario,
    generar_html_correo,
    generar_html_correo_avanzado,
)


class HashServiceTest(TestCase):
    
    def test_generar_hash_documento(self):
        pdf_content = b'contenido de prueba del PDF'
        hash_result = generar_hash_documento(pdf_content)
        
        # Verificar que es un hash SHA-256 válido (64 caracteres hex)
        self.assertEqual(len(hash_result), 64)
        self.assertTrue(all(c in '0123456789abcdef' for c in hash_result))
    
    def test_generar_hash_documento_consistente(self):
        pdf_content = b'contenido de prueba'
        hash1 = generar_hash_documento(pdf_content)
        hash2 = generar_hash_documento(pdf_content)
        self.assertEqual(hash1, hash2)
    
    def test_generar_hash_documento_diferente(self):
        hash1 = generar_hash_documento(b'contenido 1')
        hash2 = generar_hash_documento(b'contenido 2')
        self.assertNotEqual(hash1, hash2)
    
    def test_generar_hash_inventario(self):
        inventarios_data = [
            {'producto_codigo': 'PROD-001', 'cantidad': 100},
            {'producto_codigo': 'PROD-002', 'cantidad': 200},
        ]
        hash_result = generar_hash_inventario(inventarios_data)
        
        # Verificar que es un hash válido
        self.assertEqual(len(hash_result), 64)
        self.assertTrue(all(c in '0123456789abcdef' for c in hash_result))
    
    def test_generar_hash_inventario_orden_no_importa(self):
        """Test: El orden de los datos NO afecta el hash (se ordena internamente)"""
        inventarios1 = [
            {'producto_codigo': 'PROD-001', 'cantidad': 100},
            {'producto_codigo': 'PROD-002', 'cantidad': 200},
        ]
        inventarios2 = [
            {'producto_codigo': 'PROD-002', 'cantidad': 200},
            {'producto_codigo': 'PROD-001', 'cantidad': 100},
        ]
        hash1 = generar_hash_inventario(inventarios1)
        hash2 = generar_hash_inventario(inventarios2)
        # El hash debería ser IGUAL porque se ordenan internamente para consistencia
        self.assertEqual(hash1, hash2)


class HTMLCorreoServiceTest(TestCase):
    
    def setUp(self):
        self.empresa_data = {
            'nit': '900123456-1',
            'nombre': 'Empresa Test',
            'direccion': 'Calle 123',
            'telefono': '3001234567'
        }
    
    def test_generar_html_correo_basico(self):
        html = generar_html_correo(
            self.empresa_data,
            total_productos=10,
            total_unidades=500
        )
        
        # Verificar que contiene información básica
        self.assertIn('Empresa Test', html)
        self.assertIn('10', html)
        self.assertIn('500', html)
        self.assertIn('<html', html.lower())
    
    def test_generar_html_correo_avanzado(self):
        alertas = [
            {'mensaje': 'Stock bajo', 'prioridad': 'alta'},
            {'mensaje': 'Revisar precios', 'prioridad': 'media'},
        ]
        html = generar_html_correo_avanzado(
            self.empresa_data,
            total_productos=10,
            total_unidades=500,
            alertas=alertas,
            hash_documento='abc123hash'
        )
        
        # Verificar contenido
        self.assertIn('Empresa Test', html)
        self.assertIn('<html', html.lower())
    
    def test_generar_html_correo_sin_alertas(self):
        html = generar_html_correo_avanzado(
            self.empresa_data,
            total_productos=5,
            total_unidades=100,
            alertas=None,
            hash_documento=None
        )
        
        self.assertIn('Empresa Test', html)
        self.assertIn('<html', html.lower())


class PDFServiceTest(TestCase):
    
    def setUp(self):
        self.empresa_data = {
            'nit': '900123456-1',
            'nombre': 'Empresa Test',
            'direccion': 'Calle 123',
            'telefono': '3001234567'
        }
        self.inventarios_data = [
            {
                'id': 1,
                'producto_codigo': 'PROD-001',
                'producto_nombre': 'Producto 1',
                'cantidad': 100,
                'fecha_actualizacion': '2025-01-01T00:00:00'
            },
            {
                'id': 2,
                'producto_codigo': 'PROD-002',
                'producto_nombre': 'Producto 2',
                'cantidad': 200,
                'fecha_actualizacion': '2025-01-02T00:00:00'
            }
        ]
    
    def test_generar_pdf_inventario(self):
        from .email_service import generar_pdf_inventario
        
        pdf_content = generar_pdf_inventario(
            self.empresa_data,
            self.inventarios_data
        )
        
        # Verificar que es un PDF válido (empieza con %PDF)
        self.assertTrue(pdf_content.startswith(b'%PDF'))
    
    def test_generar_pdf_inventario_vacio(self):
        from .email_service import generar_pdf_inventario
        
        pdf_content = generar_pdf_inventario(
            self.empresa_data,
            []  # Sin inventarios
        )
        
        # Debe generar un PDF válido aunque esté vacío
        self.assertTrue(pdf_content.startswith(b'%PDF'))


class EmailSendServiceTest(TestCase):
    
    @patch('api.email_service.requests.post')
    def test_enviar_correo_resend_sin_api_key(self, mock_post):
        """Test: Enviar correo sin API key genera ValueError"""
        from .email_service import enviar_correo_resend
        
        # Simular que no hay API key
        with patch.dict(os.environ, {'RESEND_API_KEY': ''}, clear=False):
            with patch('api.email_service.settings') as mock_settings:
                mock_settings.RESEND_API_KEY = ''
                delattr(mock_settings, 'RESEND_API_KEY')  # Simular que no existe
                
                with self.assertRaises(ValueError):
                    enviar_correo_resend(
                        destinatario='test@example.com',
                        asunto='Test',
                        cuerpo_html='<p>Test</p>',
                        adjunto_pdf=b'%PDF',
                        nombre_archivo='test.pdf'
                    )
    
    @patch('api.email_service.requests.post')
    def test_enviar_correo_resend_exitoso(self, mock_post):
        """Test: Enviar correo exitoso usando Resend API"""
        from .email_service import enviar_correo_resend
        
        # Mock de respuesta exitosa
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'id': 'test-email-id'}
        mock_post.return_value = mock_response
        
        with patch.dict(os.environ, {'RESEND_API_KEY': 're_test_key'}, clear=False):
            result = enviar_correo_resend(
                destinatario='dest@example.com',
                asunto='Test Subject',
                cuerpo_html='<p>Test Body</p>',
                adjunto_pdf=b'%PDF-test',
                nombre_archivo='test.pdf'
            )
            
            self.assertEqual(result['id'], 'test-email-id')
            mock_post.assert_called_once()
