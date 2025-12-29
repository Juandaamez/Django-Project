"""
Repositorios Django: Implementación de Interfaces del Dominio
=============================================================

Estos repositorios implementan las interfaces definidas en la capa
de dominio, utilizando el ORM de Django para la persistencia.

Principios:
- Implementan las interfaces del dominio (Dependency Inversion)
- Usan mappers para traducir entre modelos y entidades
- Encapsulan toda la lógica de acceso a datos
"""

from typing import List, Optional

from django.db.models import Q

from core.models import Empresa as EmpresaModel
from core.models import Producto as ProductoModel
from core.models import Inventario as InventarioModel
from core.models import HistorialEnvio as HistorialEnvioModel
from core.adapters.mappers import (
    EmpresaMapper, ProductoMapper, InventarioMapper, HistorialEnvioMapper
)

# Importar interfaces del dominio
try:
    from litethinking_domain.interfaces.repositories import (
        IEmpresaRepository,
        IProductoRepository,
        IInventarioRepository,
        IHistorialEnvioRepository,
    )
    from litethinking_domain.entities import (
        Empresa, Producto, Inventario, HistorialEnvio
    )
    from litethinking_domain.value_objects import NIT, CodigoProducto, Email
    DOMAIN_AVAILABLE = True
except ImportError:
    DOMAIN_AVAILABLE = False
    # Crear clases base vacías para evitar errores de sintaxis
    class IEmpresaRepository: pass
    class IProductoRepository: pass
    class IInventarioRepository: pass
    class IHistorialEnvioRepository: pass


class DjangoEmpresaRepository(IEmpresaRepository if DOMAIN_AVAILABLE else object):
    """
    Implementación Django del repositorio de Empresas.
    
    Traduce entre el ORM de Django y las entidades de dominio,
    proporcionando una capa de abstracción limpia.
    """
    
    def obtener_por_nit(self, nit: "NIT") -> Optional["Empresa"]:
        """Obtiene una empresa por su NIT."""
        try:
            model = EmpresaModel.objects.get(nit=str(nit))
            return EmpresaMapper.to_domain(model)
        except EmpresaModel.DoesNotExist:
            return None
    
    def obtener_todas(self, solo_activas: bool = True) -> List["Empresa"]:
        """Obtiene todas las empresas."""
        queryset = EmpresaModel.objects.all()
        return [EmpresaMapper.to_domain(m) for m in queryset]
    
    def guardar(self, empresa: "Empresa") -> "Empresa":
        """Guarda (crea o actualiza) una empresa."""
        nit_str = str(empresa.nit)
        
        defaults = {
            'nombre': empresa.nombre,
            'direccion': empresa.direccion,
            'telefono': empresa.telefono,
        }
        
        model, created = EmpresaModel.objects.update_or_create(
            nit=nit_str,
            defaults=defaults
        )
        
        return EmpresaMapper.to_domain(model)
    
    def eliminar(self, nit: "NIT") -> bool:
        """Elimina una empresa por su NIT."""
        try:
            EmpresaModel.objects.get(nit=str(nit)).delete()
            return True
        except EmpresaModel.DoesNotExist:
            return False
    
    def existe(self, nit: "NIT") -> bool:
        """Verifica si existe una empresa con el NIT dado."""
        return EmpresaModel.objects.filter(nit=str(nit)).exists()
    
    def buscar(self, termino: str) -> List["Empresa"]:
        """Busca empresas por nombre o NIT."""
        queryset = EmpresaModel.objects.filter(
            Q(nombre__icontains=termino) | Q(nit__icontains=termino)
        )
        return [EmpresaMapper.to_domain(m) for m in queryset]


class DjangoProductoRepository(IProductoRepository if DOMAIN_AVAILABLE else object):
    """
    Implementación Django del repositorio de Productos.
    """
    
    def obtener_por_codigo(self, codigo: "CodigoProducto") -> Optional["Producto"]:
        """Obtiene un producto por su código."""
        try:
            model = ProductoModel.objects.select_related('empresa').get(
                codigo=str(codigo)
            )
            return ProductoMapper.to_domain(model)
        except ProductoModel.DoesNotExist:
            return None
    
    def obtener_por_empresa(self, empresa_nit: "NIT") -> List["Producto"]:
        """Obtiene todos los productos de una empresa."""
        queryset = ProductoModel.objects.filter(
            empresa__nit=str(empresa_nit)
        ).select_related('empresa')
        return [ProductoMapper.to_domain(m) for m in queryset]
    
    def obtener_todos(self, solo_activos: bool = True) -> List["Producto"]:
        """Obtiene todos los productos."""
        queryset = ProductoModel.objects.select_related('empresa').all()
        return [ProductoMapper.to_domain(m) for m in queryset]
    
    def guardar(self, producto: "Producto") -> "Producto":
        """Guarda (crea o actualiza) un producto."""
        codigo_str = str(producto.codigo)
        
        # Obtener la empresa
        try:
            empresa_model = EmpresaModel.objects.get(nit=str(producto.empresa_nit))
        except EmpresaModel.DoesNotExist:
            raise ValueError(f"No existe la empresa con NIT: {producto.empresa_nit}")
        
        # Convertir precios a JSON
        precios_json = {}
        for moneda, precio in producto.precios.items():
            precios_json[moneda] = float(precio.monto)
        
        defaults = {
            'nombre': producto.nombre,
            'caracteristicas': producto.caracteristicas,
            'precios': precios_json,
            'empresa': empresa_model,
        }
        
        model, created = ProductoModel.objects.update_or_create(
            codigo=codigo_str,
            defaults=defaults
        )
        
        return ProductoMapper.to_domain(model)
    
    def eliminar(self, codigo: "CodigoProducto") -> bool:
        """Elimina un producto por su código."""
        try:
            ProductoModel.objects.get(codigo=str(codigo)).delete()
            return True
        except ProductoModel.DoesNotExist:
            return False
    
    def existe(self, codigo: "CodigoProducto") -> bool:
        """Verifica si existe un producto con el código dado."""
        return ProductoModel.objects.filter(codigo=str(codigo)).exists()
    
    def buscar(self, termino: str, empresa_nit: Optional["NIT"] = None) -> List["Producto"]:
        """Busca productos por nombre o código."""
        queryset = ProductoModel.objects.filter(
            Q(nombre__icontains=termino) | Q(codigo__icontains=termino)
        )
        
        if empresa_nit:
            queryset = queryset.filter(empresa__nit=str(empresa_nit))
        
        return [ProductoMapper.to_domain(m) for m in queryset.select_related('empresa')]


class DjangoInventarioRepository(IInventarioRepository if DOMAIN_AVAILABLE else object):
    """
    Implementación Django del repositorio de Inventario.
    """
    
    def obtener_por_id(self, id: int) -> Optional["Inventario"]:
        """Obtiene un registro de inventario por su ID."""
        try:
            model = InventarioModel.objects.select_related('producto').get(id=id)
            return InventarioMapper.to_domain(model)
        except InventarioModel.DoesNotExist:
            return None
    
    def obtener_por_producto(self, producto_codigo: "CodigoProducto") -> Optional["Inventario"]:
        """Obtiene el inventario de un producto específico."""
        try:
            model = InventarioModel.objects.select_related('producto').get(
                producto__codigo=str(producto_codigo)
            )
            return InventarioMapper.to_domain(model)
        except InventarioModel.DoesNotExist:
            return None
    
    def obtener_por_empresa(self, empresa_nit: "NIT") -> List["Inventario"]:
        """Obtiene todo el inventario de una empresa."""
        queryset = InventarioModel.objects.filter(
            producto__empresa__nit=str(empresa_nit)
        ).select_related('producto', 'producto__empresa')
        return [InventarioMapper.to_domain(m) for m in queryset]
    
    def obtener_todos(self) -> List["Inventario"]:
        """Obtiene todo el inventario."""
        queryset = InventarioModel.objects.select_related('producto').all()
        return [InventarioMapper.to_domain(m) for m in queryset]
    
    def guardar(self, inventario: "Inventario") -> "Inventario":
        """Guarda (crea o actualiza) un registro de inventario."""
        # Obtener el producto
        try:
            producto_model = ProductoModel.objects.get(
                codigo=str(inventario.producto_codigo)
            )
        except ProductoModel.DoesNotExist:
            raise ValueError(f"No existe el producto: {inventario.producto_codigo}")
        
        if inventario.id:
            # Actualizar existente
            model = InventarioModel.objects.get(id=inventario.id)
            model.cantidad = inventario.cantidad
            model.save()
        else:
            # Crear o actualizar por producto
            model, _ = InventarioModel.objects.update_or_create(
                producto=producto_model,
                defaults={'cantidad': inventario.cantidad}
            )
        
        return InventarioMapper.to_domain(model)
    
    def eliminar(self, id: int) -> bool:
        """Elimina un registro de inventario."""
        try:
            InventarioModel.objects.get(id=id).delete()
            return True
        except InventarioModel.DoesNotExist:
            return False
    
    def obtener_bajo_stock(self) -> List["Inventario"]:
        """Obtiene productos con stock bajo (menos de 10 unidades)."""
        queryset = InventarioModel.objects.filter(
            cantidad__gt=0, cantidad__lt=10
        ).select_related('producto')
        return [InventarioMapper.to_domain(m) for m in queryset]
    
    def obtener_agotados(self) -> List["Inventario"]:
        """Obtiene productos sin stock."""
        queryset = InventarioModel.objects.filter(
            cantidad=0
        ).select_related('producto')
        return [InventarioMapper.to_domain(m) for m in queryset]


class DjangoHistorialEnvioRepository(IHistorialEnvioRepository if DOMAIN_AVAILABLE else object):
    """
    Implementación Django del repositorio de Historial de Envíos.
    """
    
    def obtener_por_id(self, id: int) -> Optional["HistorialEnvio"]:
        """Obtiene un registro de historial por su ID."""
        try:
            model = HistorialEnvioModel.objects.select_related(
                'empresa', 'usuario'
            ).get(id=id)
            return HistorialEnvioMapper.to_domain(model)
        except HistorialEnvioModel.DoesNotExist:
            return None
    
    def obtener_por_empresa(self, empresa_nit: "NIT") -> List["HistorialEnvio"]:
        """Obtiene el historial de envíos de una empresa."""
        queryset = HistorialEnvioModel.objects.filter(
            empresa__nit=str(empresa_nit)
        ).select_related('empresa', 'usuario').order_by('-fecha_creacion')
        return [HistorialEnvioMapper.to_domain(m) for m in queryset]
    
    def obtener_por_email(self, email: "Email") -> List["HistorialEnvio"]:
        """Obtiene el historial de envíos a un email específico."""
        queryset = HistorialEnvioModel.objects.filter(
            email_destino=str(email)
        ).select_related('empresa', 'usuario').order_by('-fecha_creacion')
        return [HistorialEnvioMapper.to_domain(m) for m in queryset]
    
    def guardar(self, historial: "HistorialEnvio") -> "HistorialEnvio":
        """Guarda un nuevo registro de historial."""
        # Obtener la empresa
        try:
            empresa_model = EmpresaModel.objects.get(nit=str(historial.empresa_nit))
        except EmpresaModel.DoesNotExist:
            raise ValueError(f"No existe la empresa: {historial.empresa_nit}")
        
        # Obtener usuario si existe
        usuario = None
        if historial.usuario_id:
            from django.contrib.auth.models import User
            try:
                usuario = User.objects.get(id=historial.usuario_id)
            except User.DoesNotExist:
                pass
        
        model = HistorialEnvioMapper.to_model(historial, empresa_model, usuario)
        model.save()
        
        return HistorialEnvioMapper.to_domain(model)
    
    def verificar_por_hash(self, hash_documento: str) -> Optional["HistorialEnvio"]:
        """Verifica la autenticidad de un documento por su hash."""
        try:
            model = HistorialEnvioModel.objects.select_related(
                'empresa', 'usuario'
            ).get(documento_hash=hash_documento)
            return HistorialEnvioMapper.to_domain(model)
        except HistorialEnvioModel.DoesNotExist:
            return None
    
    def obtener_ultimos(self, limite: int = 10) -> List["HistorialEnvio"]:
        """Obtiene los últimos registros del historial."""
        queryset = HistorialEnvioModel.objects.select_related(
            'empresa', 'usuario'
        ).order_by('-fecha_creacion')[:limite]
        return [HistorialEnvioMapper.to_domain(m) for m in queryset]
