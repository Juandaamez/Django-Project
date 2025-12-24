from rest_framework.routers import DefaultRouter

from .views import EmpresaViewSet, InventarioViewSet, ProductoViewSet

router = DefaultRouter()
router.register('empresas', EmpresaViewSet, basename='empresa')
router.register('productos', ProductoViewSet, basename='producto')
router.register('inventarios', InventarioViewSet, basename='inventario')

urlpatterns = router.urls
