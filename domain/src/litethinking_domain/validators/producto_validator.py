"""
Validador de Producto
=====================

Reglas de negocio para la entidad Producto.
"""

from typing import List, Optional, Dict
from decimal import Decimal

from litethinking_domain.entities import Producto
from litethinking_domain.value_objects import Money, CodigoProducto
from litethinking_domain.exceptions import ValidacionError
from litethinking_domain.validators.empresa_validator import ResultadoValidacion


class ValidadorProducto:
    """
    Validador de reglas de negocio para Producto.
    
    Encapsula todas las reglas de validación para mantener
    las entidades limpias y las reglas centralizadas.
    """
    
    # Constantes de validación
    NOMBRE_MIN_LENGTH = 2
    NOMBRE_MAX_LENGTH = 150
    CODIGO_MIN_LENGTH = 2
    CODIGO_MAX_LENGTH = 50
    CARACTERISTICAS_MAX_LENGTH = 2000
    PRECIO_MINIMO = Decimal("0.01")
    PRECIO_MAXIMO = Decimal("999999999.99")
    MONEDAS_SOPORTADAS = {"COP", "USD", "EUR", "MXN", "BRL"}
    
    def validar(self, producto: Producto) -> ResultadoValidacion:
        """
        Valida todas las reglas de negocio para un producto.
        
        Args:
            producto: Producto a validar
            
        Returns:
            ResultadoValidacion con el estado y errores encontrados
        """
        errores: List[ValidacionError] = []
        
        # Validar nombre
        error_nombre = self._validar_nombre(producto.nombre)
        if error_nombre:
            errores.append(error_nombre)
        
        # Validar características
        error_caracteristicas = self._validar_caracteristicas(producto.caracteristicas)
        if error_caracteristicas:
            errores.append(error_caracteristicas)
        
        # Validar precios
        errores_precios = self._validar_precios(producto.precios)
        errores.extend(errores_precios)
        
        return ResultadoValidacion(
            valido=len(errores) == 0,
            errores=errores
        )
    
    def _validar_nombre(self, nombre: str) -> Optional[ValidacionError]:
        """Valida el nombre del producto."""
        if not nombre or not nombre.strip():
            return ValidacionError("nombre", "El nombre es requerido")
        
        nombre_limpio = nombre.strip()
        
        if len(nombre_limpio) < self.NOMBRE_MIN_LENGTH:
            return ValidacionError(
                "nombre",
                f"El nombre debe tener al menos {self.NOMBRE_MIN_LENGTH} caracteres"
            )
        
        if len(nombre_limpio) > self.NOMBRE_MAX_LENGTH:
            return ValidacionError(
                "nombre",
                f"El nombre no puede exceder {self.NOMBRE_MAX_LENGTH} caracteres"
            )
        
        return None
    
    def _validar_caracteristicas(self, caracteristicas: str) -> Optional[ValidacionError]:
        """Valida las características del producto."""
        if caracteristicas and len(caracteristicas) > self.CARACTERISTICAS_MAX_LENGTH:
            return ValidacionError(
                "caracteristicas",
                f"Las características no pueden exceder {self.CARACTERISTICAS_MAX_LENGTH} caracteres"
            )
        
        return None
    
    def _validar_precios(self, precios: Dict[str, Money]) -> List[ValidacionError]:
        """Valida los precios del producto."""
        errores = []
        
        if not precios:
            errores.append(ValidacionError(
                "precios",
                "El producto debe tener al menos un precio definido"
            ))
            return errores
        
        for moneda, precio in precios.items():
            # Validar moneda soportada
            if moneda.upper() not in self.MONEDAS_SOPORTADAS:
                errores.append(ValidacionError(
                    f"precios.{moneda}",
                    f"Moneda no soportada: {moneda}. "
                    f"Monedas válidas: {', '.join(self.MONEDAS_SOPORTADAS)}"
                ))
                continue
            
            # Validar monto mínimo
            if precio.monto < self.PRECIO_MINIMO:
                errores.append(ValidacionError(
                    f"precios.{moneda}",
                    f"El precio en {moneda} debe ser al menos {self.PRECIO_MINIMO}"
                ))
            
            # Validar monto máximo
            if precio.monto > self.PRECIO_MAXIMO:
                errores.append(ValidacionError(
                    f"precios.{moneda}",
                    f"El precio en {moneda} no puede exceder {self.PRECIO_MAXIMO}"
                ))
        
        return errores
    
    def validar_codigo(self, codigo_str: str) -> ResultadoValidacion:
        """
        Valida un código de producto antes de crear la entidad.
        
        Args:
            codigo_str: String del código a validar
        """
        errores = []
        
        try:
            CodigoProducto(codigo_str)
        except ValueError as e:
            errores.append(ValidacionError("codigo", str(e)))
        
        return ResultadoValidacion(
            valido=len(errores) == 0,
            errores=errores
        )
    
    def validar_precio_individual(
        self,
        monto: float,
        moneda: str
    ) -> ResultadoValidacion:
        """
        Valida un precio individual.
        
        Args:
            monto: Monto del precio
            moneda: Código de moneda
        """
        errores = []
        
        if moneda.upper() not in self.MONEDAS_SOPORTADAS:
            errores.append(ValidacionError(
                "moneda",
                f"Moneda no soportada: {moneda}"
            ))
        
        if monto <= 0:
            errores.append(ValidacionError(
                "monto",
                "El precio debe ser mayor a cero"
            ))
        
        if monto > float(self.PRECIO_MAXIMO):
            errores.append(ValidacionError(
                "monto",
                f"El precio no puede exceder {self.PRECIO_MAXIMO}"
            ))
        
        return ResultadoValidacion(
            valido=len(errores) == 0,
            errores=errores
        )
    
    def puede_eliminar(
        self,
        producto: Producto,
        tiene_inventario: bool,
        cantidad_inventario: int = 0
    ) -> ResultadoValidacion:
        """
        Valida si un producto puede ser eliminado.
        
        Args:
            producto: Producto a eliminar
            tiene_inventario: Si el producto tiene registro de inventario
            cantidad_inventario: Cantidad actual en inventario
        """
        errores = []
        
        if tiene_inventario and cantidad_inventario > 0:
            errores.append(ValidacionError(
                "producto",
                f"No se puede eliminar un producto con {cantidad_inventario} "
                "unidades en inventario. Primero reduzca el stock a cero."
            ))
        
        return ResultadoValidacion(
            valido=len(errores) == 0,
            errores=errores
        )
