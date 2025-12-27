from django.urls import path
from rest_framework.routers import DefaultRouter

from .authentication import LoginView
from .views import (
	EmpresaViewSet,
	InventarioViewSet,
	ProductoViewSet,
	GenerarPDFView,
	EnviarCorreoInventarioView,
	HistorialEnviosViewSet,
	AnalisisInventarioView,
)

router = DefaultRouter()
router.register('empresas', EmpresaViewSet, basename='empresa')
router.register('productos', ProductoViewSet, basename='producto')
router.register('inventarios', InventarioViewSet, basename='inventario')
router.register('historial-envios', HistorialEnviosViewSet, basename='historial-envio')

urlpatterns = [
	path('auth/login/', LoginView.as_view(), name='auth-login'),
	# Endpoints para PDF y correo
	path('inventarios/pdf/<str:empresa_nit>/', GenerarPDFView.as_view(), name='inventario-pdf'),
	path('inventarios/enviar-correo/', EnviarCorreoInventarioView.as_view(), name='inventario-enviar-correo'),
	path('inventarios/analisis/<str:empresa_nit>/', AnalisisInventarioView.as_view(), name='inventario-analisis'),
]

urlpatterns += router.urls
