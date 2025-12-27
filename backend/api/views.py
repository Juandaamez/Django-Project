import base64
import json
from datetime import datetime

from django.http import HttpResponse
from rest_framework import filters, permissions, viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Empresa, Inventario, Producto, HistorialEnvio
from .serializers import (
	EmpresaSerializer,
	InventarioSerializer,
	ProductoSerializer,
	HistorialEnvioSerializer,
)
from .email_service import (
	generar_pdf_inventario,
	generar_html_correo,
	generar_html_correo_avanzado,
	enviar_correo_resend,
	enviar_correo_django,
	generar_hash_documento,
	generar_hash_inventario,
)
from .ia_service import analizar_inventario, generar_resumen_para_correo


class IsAdminOrReadOnly(permissions.BasePermission):
	message = 'Solo los administradores pueden modificar los registros.'

	def has_permission(self, request, view):
		if request.method in permissions.SAFE_METHODS:
			return True
		return bool(request.user and request.user.is_staff)


class EmpresaViewSet(viewsets.ModelViewSet):
	queryset = Empresa.objects.all().order_by('nombre')
	serializer_class = EmpresaSerializer
	permission_classes = [IsAdminOrReadOnly]
	filter_backends = [filters.SearchFilter, filters.OrderingFilter]
	search_fields = ['nit', 'nombre', 'direccion']
	ordering_fields = ['nombre', 'nit']
	ordering = ['nombre']


class ProductoViewSet(viewsets.ModelViewSet):
	queryset = Producto.objects.select_related('empresa').all()
	serializer_class = ProductoSerializer
	permission_classes = [IsAdminOrReadOnly]  # Público para leer, admin para modificar
	filter_backends = [filters.SearchFilter, filters.OrderingFilter]
	search_fields = ['codigo', 'nombre', 'caracteristicas', 'empresa__nombre']
	ordering_fields = ['nombre', 'codigo', 'empresa__nombre']
	ordering = ['nombre']

	def get_queryset(self):
		queryset = super().get_queryset()
		empresa_nit = self.request.query_params.get('empresa')
		if empresa_nit:
			queryset = queryset.filter(empresa__nit=empresa_nit)
		return queryset

	def create(self, request, *args, **kwargs):
		"""
		Al crear un producto, automáticamente crear un registro en Inventario
		con la cantidad inicial especificada (default 0)
		"""
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		producto = serializer.save()

		# Obtener cantidad inicial del request (opcional, default 0)
		cantidad_inicial = request.data.get('cantidad_inicial', 0)
		
		# Crear registro de inventario automáticamente
		Inventario.objects.create(
			producto=producto,
			cantidad=cantidad_inicial
		)

		headers = self.get_success_headers(serializer.data)
		return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class InventarioViewSet(viewsets.ModelViewSet):
	queryset = (
		Inventario.objects.select_related('producto', 'producto__empresa')
		.all()
	)
	serializer_class = InventarioSerializer
	permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
	filter_backends = [filters.SearchFilter, filters.OrderingFilter]
	search_fields = [
		'producto__codigo',
		'producto__nombre',
		'producto__empresa__nombre',
	]
	ordering_fields = ['fecha_actualizacion', 'producto__nombre']
	ordering = ['-fecha_actualizacion']

	def get_queryset(self):
		queryset = super().get_queryset()
		empresa_nit = self.request.query_params.get('empresa')
		producto_codigo = self.request.query_params.get('producto')
		if empresa_nit:
			queryset = queryset.filter(producto__empresa__nit=empresa_nit)
		if producto_codigo:
			queryset = queryset.filter(producto__codigo=producto_codigo)
		return queryset


class GenerarPDFView(APIView):
	"""
	Vista para generar PDF del inventario de una empresa
	GET /api/inventarios/pdf/{empresa_nit}/
	"""
	permission_classes = [IsAuthenticated]

	def get(self, request, empresa_nit):
		try:
			# Obtener empresa
			empresa = Empresa.objects.get(nit=empresa_nit)
			empresa_data = {
				'nit': empresa.nit,
				'nombre': empresa.nombre,
				'direccion': empresa.direccion,
				'telefono': empresa.telefono,
			}
			
			# Obtener inventarios
			inventarios = Inventario.objects.filter(
				producto__empresa__nit=empresa_nit
			).select_related('producto')
			
			inventarios_data = []
			for inv in inventarios:
				inventarios_data.append({
					'id': inv.id,
					'producto_codigo': inv.producto.codigo,
					'producto_nombre': inv.producto.nombre,
					'cantidad': inv.cantidad,
					'fecha_actualizacion': inv.fecha_actualizacion.isoformat() if inv.fecha_actualizacion else None,
				})
			
			# Generar PDF
			pdf_content = generar_pdf_inventario(empresa_data, inventarios_data)
			
			# Retornar PDF
			response = HttpResponse(pdf_content, content_type='application/pdf')
			filename = f"Inventario_{empresa.nombre.replace(' ', '_')}_{empresa_nit}.pdf"
			response['Content-Disposition'] = f'attachment; filename="{filename}"'
			return response
			
		except Empresa.DoesNotExist:
			return Response(
				{'error': 'Empresa no encontrada'},
				status=status.HTTP_404_NOT_FOUND
			)
		except Exception as e:
			return Response(
				{'error': str(e)},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)


class EnviarCorreoInventarioView(APIView):
	"""
	Vista para enviar el PDF del inventario por correo
	
	POST /api/inventarios/enviar-correo/
	
	Body:
	{
		empresa_nit: string (requerido),
		email_destino: string (requerido),
		pdf_base64: string (opcional - PDF generado en frontend),
		incluir_analisis_ia: boolean (opcional - incluir análisis inteligente),
		incluir_blockchain: boolean (opcional - incluir certificación blockchain)
	}
	
	Funcionalidades:
	- Generación de PDF profesional
	- Análisis inteligente con IA (alertas, recomendaciones)
	- Certificación Blockchain con hash SHA-256
	- Historial de envíos
	- Envío via Resend API o Django SMTP
	"""
	permission_classes = [IsAuthenticated]

	def post(self, request):
		try:
			# Obtener parámetros
			empresa_nit = request.data.get('empresa_nit')
			email_destino = request.data.get('email_destino')
			pdf_base64 = request.data.get('pdf_base64')
			incluir_analisis_ia = request.data.get('incluir_analisis_ia', True)
			incluir_blockchain = request.data.get('incluir_blockchain', True)
			
			# Validaciones
			if not empresa_nit:
				return Response(
					{'error': 'Se requiere el NIT de la empresa'},
					status=status.HTTP_400_BAD_REQUEST
				)
			
			if not email_destino:
				return Response(
					{'error': 'Se requiere el correo de destino'},
					status=status.HTTP_400_BAD_REQUEST
				)
			
			# Obtener empresa
			empresa = Empresa.objects.get(nit=empresa_nit)
			empresa_data = {
				'nit': empresa.nit,
				'nombre': empresa.nombre,
				'direccion': empresa.direccion,
				'telefono': empresa.telefono,
			}
			
			# Obtener inventarios con precios
			inventarios = Inventario.objects.filter(
				producto__empresa__nit=empresa_nit
			).select_related('producto')
			
			inventarios_data = []
			valor_total = 0
			for inv in inventarios:
				precio = 0
				if inv.producto.precios:
					try:
						precios = inv.producto.precios if isinstance(inv.producto.precios, dict) else json.loads(inv.producto.precios)
						precio = precios.get('COP', precios.get('USD', 0))
					except:
						pass
				
				valor_total += inv.cantidad * precio
				inventarios_data.append({
					'id': inv.id,
					'producto_codigo': inv.producto.codigo,
					'producto_nombre': inv.producto.nombre,
					'producto_precio': precio,
					'cantidad': inv.cantidad,
					'fecha_actualizacion': inv.fecha_actualizacion.isoformat() if inv.fecha_actualizacion else None,
				})
			
			# Generar PDF
			if pdf_base64:
				pdf_content = base64.b64decode(pdf_base64)
			else:
				pdf_content = generar_pdf_inventario(empresa_data, inventarios_data)
			
			# Calcular estadísticas
			total_productos = len(inventarios_data)
			total_unidades = sum(inv['cantidad'] for inv in inventarios_data)
			
			# ═══════════════════════════════════════════════════════════
			# ANÁLISIS IA
			# ═══════════════════════════════════════════════════════════
			alertas = []
			resumen_ia = ""
			if incluir_analisis_ia:
				try:
					resumen_ia, alertas = generar_resumen_para_correo(empresa_data, inventarios_data)
				except Exception as ia_error:
					print(f"Error en análisis IA: {ia_error}")
			
			# ═══════════════════════════════════════════════════════════
			# CERTIFICACIÓN BLOCKCHAIN
			# ═══════════════════════════════════════════════════════════
			hash_documento = None
			hash_contenido = None
			if incluir_blockchain:
				hash_documento = generar_hash_documento(pdf_content)
				hash_contenido = generar_hash_inventario(inventarios_data)
			
			# ═══════════════════════════════════════════════════════════
			# GENERAR HTML DEL CORREO
			# ═══════════════════════════════════════════════════════════
			if incluir_analisis_ia or incluir_blockchain:
				html_correo = generar_html_correo_avanzado(
					empresa_data,
					total_productos,
					total_unidades,
					alertas=alertas if incluir_analisis_ia else None,
					hash_documento=hash_documento if incluir_blockchain else None
				)
			else:
				html_correo = generar_html_correo(empresa_data, total_productos, total_unidades)
			
			# Asunto del correo
			asunto = f"📦 Reporte de Inventario - {empresa.nombre}"
			if alertas:
				criticas = len([a for a in alertas if a.get('prioridad') == 'critica'])
				if criticas > 0:
					asunto = f"⚠️ Reporte de Inventario (Alertas) - {empresa.nombre}"
			
			# Nombre del archivo
			nombre_archivo = f"Inventario_{empresa.nombre.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
			
			# ═══════════════════════════════════════════════════════════
			# CREAR REGISTRO DE HISTORIAL
			# ═══════════════════════════════════════════════════════════
			historial = HistorialEnvio.objects.create(
				empresa=empresa,
				usuario=request.user,
				email_destino=email_destino,
				asunto=asunto,
				estado='pendiente',
				documento_hash=hash_documento or '',
				contenido_hash=hash_contenido or '',
				total_productos=total_productos,
				total_unidades=total_unidades,
				valor_inventario=valor_total,
				resumen_ia=resumen_ia,
				alertas_ia=alertas,
			)
			
			# ═══════════════════════════════════════════════════════════
			# ENVIAR CORREO
			# ═══════════════════════════════════════════════════════════
			try:
				resultado = enviar_correo_resend(
					destinatario=email_destino,
					asunto=asunto,
					cuerpo_html=html_correo,
					adjunto_pdf=pdf_content,
					nombre_archivo=nombre_archivo
				)
				
				# Actualizar historial
				historial.estado = 'enviado'
				historial.proveedor = 'resend'
				historial.respuesta_api = resultado
				historial.fecha_envio = datetime.now()
				historial.save()
				
				return Response({
					'success': True,
					'message': f'Correo enviado exitosamente a {email_destino}',
					'provider': 'resend',
					'historial_id': historial.id,
					'hash_documento': hash_documento,
					'alertas_count': len(alertas),
					'details': resultado
				})
				
			except ValueError as ve:
				# Si no hay API key de Resend, intentar con Django Email
				try:
					enviados = enviar_correo_django(
						destinatario=email_destino,
						asunto=asunto,
						cuerpo=html_correo,
						adjunto_pdf=pdf_content,
						nombre_archivo=nombre_archivo
					)
					
					if enviados > 0:
						historial.estado = 'enviado'
						historial.proveedor = 'django_smtp'
						historial.fecha_envio = datetime.now()
						historial.save()
						
						return Response({
							'success': True,
							'message': f'Correo enviado exitosamente a {email_destino}',
							'provider': 'django_smtp',
							'historial_id': historial.id,
							'hash_documento': hash_documento,
							'alertas_count': len(alertas)
						})
					else:
						historial.estado = 'fallido'
						historial.mensaje_error = 'No se pudo enviar el correo (0 enviados)'
						historial.save()
						
						return Response({
							'success': False,
							'error': 'No se pudo enviar el correo',
							'suggestion': 'Configura RESEND_API_KEY o las credenciales SMTP de Django'
						}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
						
				except Exception as smtp_error:
					historial.estado = 'fallido'
					historial.mensaje_error = str(smtp_error)
					historial.save()
					
					return Response({
						'success': False,
						'error': f'Error enviando correo: {str(smtp_error)}',
						'suggestion': 'Configura RESEND_API_KEY en las variables de entorno o settings.py'
					}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
			
		except Empresa.DoesNotExist:
			return Response(
				{'error': 'Empresa no encontrada'},
				status=status.HTTP_404_NOT_FOUND
			)
		except Exception as e:
			return Response(
				{'error': str(e)},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)


class HistorialEnviosViewSet(viewsets.ReadOnlyModelViewSet):
	"""
	ViewSet para consultar el historial de envíos de inventario.
	Solo lectura - los registros se crean automáticamente al enviar correos.
	
	GET /api/historial-envios/ - Lista todos los envíos
	GET /api/historial-envios/{id}/ - Detalle de un envío
	GET /api/historial-envios/?empresa={nit} - Filtrar por empresa
	"""
	queryset = HistorialEnvio.objects.select_related('empresa', 'usuario').all()
	serializer_class = HistorialEnvioSerializer
	permission_classes = [IsAuthenticated]
	filter_backends = [filters.SearchFilter, filters.OrderingFilter]
	search_fields = ['empresa__nombre', 'email_destino', 'documento_hash']
	ordering_fields = ['fecha_creacion', 'fecha_envio']
	ordering = ['-fecha_creacion']
	
	def get_queryset(self):
		queryset = super().get_queryset()
		empresa_nit = self.request.query_params.get('empresa')
		if empresa_nit:
			queryset = queryset.filter(empresa__nit=empresa_nit)
		return queryset


class AnalisisInventarioView(APIView):
	"""
	Vista para obtener análisis IA del inventario sin enviar correo.
	
	GET /api/inventarios/analisis/{empresa_nit}/
	
	Returns:
		Análisis completo con métricas, alertas y recomendaciones
	"""
	permission_classes = [IsAuthenticated]
	
	def get(self, request, empresa_nit):
		try:
			empresa = Empresa.objects.get(nit=empresa_nit)
			empresa_data = {
				'nit': empresa.nit,
				'nombre': empresa.nombre,
				'direccion': empresa.direccion,
				'telefono': empresa.telefono,
			}
			
			inventarios = Inventario.objects.filter(
				producto__empresa__nit=empresa_nit
			).select_related('producto')
			
			inventarios_data = []
			for inv in inventarios:
				precio = 0
				if inv.producto.precios:
					try:
						precios = inv.producto.precios if isinstance(inv.producto.precios, dict) else json.loads(inv.producto.precios)
						precio = precios.get('COP', precios.get('USD', 0))
					except:
						pass
				
				inventarios_data.append({
					'producto_codigo': inv.producto.codigo,
					'producto_nombre': inv.producto.nombre,
					'producto_precio': precio,
					'cantidad': inv.cantidad,
				})
			
			# Generar análisis IA
			analisis = analizar_inventario(empresa_data, inventarios_data)
			
			return Response({
				'success': True,
				'analisis': analisis
			})
			
		except Empresa.DoesNotExist:
			return Response(
				{'error': 'Empresa no encontrada'},
				status=status.HTTP_404_NOT_FOUND
			)
		except Exception as e:
			return Response(
				{'error': str(e)},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)
