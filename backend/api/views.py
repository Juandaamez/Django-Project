from rest_framework import filters, permissions, viewsets, status
from rest_framework.response import Response

from core.models import Empresa, Inventario, Producto
from .serializers import (
	EmpresaSerializer,
	InventarioSerializer,
	ProductoSerializer,
)


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
