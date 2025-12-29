from abc import ABC, abstractmethod
from typing import List, Optional

from litethinking_domain.entities import Empresa, Producto, Inventario, HistorialEnvio
from litethinking_domain.value_objects import NIT, CodigoProducto, Email


class IEmpresaRepository(ABC):
    
    @abstractmethod
    def obtener_por_nit(self, nit: NIT) -> Optional[Empresa]:
        """Obtiene una empresa por su NIT."""
        pass
    
    @abstractmethod
    def obtener_todas(self, solo_activas: bool = True) -> List[Empresa]:
        """Obtiene todas las empresas."""
        pass
    
    @abstractmethod
    def guardar(self, empresa: Empresa) -> Empresa:
        """Guarda (crea o actualiza) una empresa."""
        pass
    
    @abstractmethod
    def eliminar(self, nit: NIT) -> bool:
        """Elimina una empresa por su NIT."""
        pass
    
    @abstractmethod
    def existe(self, nit: NIT) -> bool:
        """Verifica si existe una empresa con el NIT dado."""
        pass
    
    @abstractmethod
    def buscar(self, termino: str) -> List[Empresa]:
        """Busca empresas por nombre o NIT."""
        pass


class IProductoRepository(ABC):
    """
    Interfaz del repositorio de Productos.
    
    Define las operaciones de persistencia para la entidad Producto.
    """
    
    @abstractmethod
    def obtener_por_codigo(self, codigo: CodigoProducto) -> Optional[Producto]:
        """Obtiene un producto por su código."""
        pass
    
    @abstractmethod
    def obtener_por_empresa(self, empresa_nit: NIT) -> List[Producto]:
        """Obtiene todos los productos de una empresa."""
        pass
    
    @abstractmethod
    def obtener_todos(self, solo_activos: bool = True) -> List[Producto]:
        """Obtiene todos los productos."""
        pass
    
    @abstractmethod
    def guardar(self, producto: Producto) -> Producto:
        """Guarda (crea o actualiza) un producto."""
        pass
    
    @abstractmethod
    def eliminar(self, codigo: CodigoProducto) -> bool:
        """Elimina un producto por su código."""
        pass
    
    @abstractmethod
    def existe(self, codigo: CodigoProducto) -> bool:
        """Verifica si existe un producto con el código dado."""
        pass
    
    @abstractmethod
    def buscar(self, termino: str, empresa_nit: Optional[NIT] = None) -> List[Producto]:
        """Busca productos por nombre o código, opcionalmente filtrado por empresa."""
        pass


class IInventarioRepository(ABC):
    """
    Interfaz del repositorio de Inventario.
    
    Define las operaciones de persistencia para la entidad Inventario.
    """
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Inventario]:
        """Obtiene un registro de inventario por su ID."""
        pass
    
    @abstractmethod
    def obtener_por_producto(self, producto_codigo: CodigoProducto) -> Optional[Inventario]:
        """Obtiene el inventario de un producto específico."""
        pass
    
    @abstractmethod
    def obtener_por_empresa(self, empresa_nit: NIT) -> List[Inventario]:
        """Obtiene todo el inventario de una empresa."""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Inventario]:
        """Obtiene todo el inventario."""
        pass
    
    @abstractmethod
    def guardar(self, inventario: Inventario) -> Inventario:
        """Guarda (crea o actualiza) un registro de inventario."""
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina un registro de inventario."""
        pass
    
    @abstractmethod
    def obtener_bajo_stock(self) -> List[Inventario]:
        """Obtiene productos con stock por debajo del mínimo."""
        pass
    
    @abstractmethod
    def obtener_agotados(self) -> List[Inventario]:
        """Obtiene productos sin stock."""
        pass


class IHistorialEnvioRepository(ABC):
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[HistorialEnvio]:
        """Obtiene un registro de historial por su ID."""
        pass
    
    @abstractmethod
    def obtener_por_empresa(self, empresa_nit: NIT) -> List[HistorialEnvio]:
        """Obtiene el historial de envíos de una empresa."""
        pass
    
    @abstractmethod
    def obtener_por_email(self, email: Email) -> List[HistorialEnvio]:
        """Obtiene el historial de envíos a un email específico."""
        pass
    
    @abstractmethod
    def guardar(self, historial: HistorialEnvio) -> HistorialEnvio:
        """Guarda un nuevo registro de historial."""
        pass
    
    @abstractmethod
    def verificar_por_hash(self, hash_documento: str) -> Optional[HistorialEnvio]:
        """Verifica la autenticidad de un documento por su hash."""
        pass
    
    @abstractmethod
    def obtener_ultimos(self, limite: int = 10) -> List[HistorialEnvio]:
        """Obtiene los últimos registros del historial."""
        pass
