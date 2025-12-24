from django.urls import path
from rest_framework.routers import DefaultRouter

from .authentication import LoginView
from .views import EmpresaViewSet, InventarioViewSet, ProductoViewSet

router = DefaultRouter()
router.register('empresas', EmpresaViewSet, basename='empresa')
router.register('productos', ProductoViewSet, basename='producto')
router.register('inventarios', InventarioViewSet, basename='inventario')

urlpatterns = [
	path('auth/login/', LoginView.as_view(), name='auth-login'),
]

urlpatterns += router.urls
