"""
Validador de Inventario
=======================

Reglas de negocio para la entidad Inventario.
"""

from typing import List, Optional

from litethinking_domain.entities import Inventario
from litethinking_domain.exceptions import ValidacionError
from litethinking_domain.validators.empresa_validator import ResultadoValidacion


class ValidadorInventario:
    """
    Validador de reglas de negocio para Inventario.
    
    Encapsula todas las reglas de validación para mantener
    las entidades limpias y las reglas centralizadas.
    """
    
    # Constantes de validación
    CANTIDAD_MAXIMA = 999999999
    CANTIDAD_MINIMA_ALERTA_DEFAULT = 10
    
    def validar(self, inventario: Inventario) -> ResultadoValidacion:
        """
        Valida todas las reglas de negocio para un inventario.
        
        Args:
            inventario: Inventario a validar
            
        Returns:
            ResultadoValidacion con el estado y errores encontrados
        """
        errores: List[ValidacionError] = []
        
        # Validar cantidad
        error_cantidad = self._validar_cantidad(inventario.cantidad)
        if error_cantidad:
            errores.append(error_cantidad)
        
        # Validar cantidad mínima
        error_cantidad_minima = self._validar_cantidad_minima(inventario.cantidad_minima)
        if error_cantidad_minima:
            errores.append(error_cantidad_minima)
        
        # Validar coherencia cantidad vs cantidad_minima
        error_coherencia = self._validar_coherencia_cantidades(
            inventario.cantidad,
            inventario.cantidad_minima
        )
        if error_coherencia:
            errores.append(error_coherencia)
        
        return ResultadoValidacion(
            valido=len(errores) == 0,
            errores=errores
        )
    
    def _validar_cantidad(self, cantidad: int) -> Optional[ValidacionError]:
        """Valida la cantidad en inventario."""
        if cantidad < 0:
            return ValidacionError(
                "cantidad",
                "La cantidad no puede ser negativa"
            )
        
        if cantidad > self.CANTIDAD_MAXIMA:
            return ValidacionError(
                "cantidad",
                f"La cantidad no puede exceder {self.CANTIDAD_MAXIMA:,}"
            )
        
        return None
    
    def _validar_cantidad_minima(self, cantidad_minima: int) -> Optional[ValidacionError]:
        """Valida la cantidad mínima de alerta."""
        if cantidad_minima < 0:
            return ValidacionError(
                "cantidad_minima",
                "La cantidad mínima no puede ser negativa"
            )
        
        if cantidad_minima > self.CANTIDAD_MAXIMA:
            return ValidacionError(
                "cantidad_minima",
                f"La cantidad mínima no puede exceder {self.CANTIDAD_MAXIMA:,}"
            )
        
        return None
    
    def _validar_coherencia_cantidades(
        self,
        cantidad: int,
        cantidad_minima: int
    ) -> Optional[ValidacionError]:
        """Valida la coherencia entre cantidad y cantidad mínima."""
        # Esta es una advertencia, no un error bloqueante
        # La lógica de negocio puede decidir si esto es un problema
        return None
    
    def validar_movimiento_stock(
        self,
        inventario: Inventario,
        cantidad_movimiento: int,
        es_entrada: bool = True
    ) -> ResultadoValidacion:
        """
        Valida un movimiento de stock (entrada o salida).
        
        Args:
            inventario: Inventario actual
            cantidad_movimiento: Cantidad a mover
            es_entrada: True si es entrada, False si es salida
        """
        errores = []
        
        if cantidad_movimiento <= 0:
            errores.append(ValidacionError(
                "cantidad",
                "La cantidad del movimiento debe ser mayor a cero"
            ))
            return ResultadoValidacion(valido=False, errores=errores)
        
        if es_entrada:
            # Validar que no exceda el máximo
            nueva_cantidad = inventario.cantidad + cantidad_movimiento
            if nueva_cantidad > self.CANTIDAD_MAXIMA:
                errores.append(ValidacionError(
                    "cantidad",
                    f"El movimiento excedería el máximo permitido ({self.CANTIDAD_MAXIMA:,})"
                ))
        else:
            # Validar que hay suficiente stock
            if cantidad_movimiento > inventario.cantidad:
                errores.append(ValidacionError(
                    "cantidad",
                    f"Stock insuficiente. Disponible: {inventario.cantidad}, "
                    f"Solicitado: {cantidad_movimiento}"
                ))
        
        return ResultadoValidacion(
            valido=len(errores) == 0,
            errores=errores
        )
    
    def obtener_alertas(self, inventario: Inventario) -> List[str]:
        """
        Genera alertas basadas en el estado del inventario.
        
        Args:
            inventario: Inventario a analizar
            
        Returns:
            Lista de mensajes de alerta
        """
        alertas = []
        
        if inventario.esta_agotado:
            alertas.append(
                f"⚠️ CRÍTICO: Producto {inventario.producto_codigo} agotado (0 unidades)"
            )
        elif inventario.requiere_reposicion:
            alertas.append(
                f"⚡ ALERTA: Producto {inventario.producto_codigo} bajo stock "
                f"({inventario.cantidad} de mínimo {inventario.cantidad_minima})"
            )
        
        return alertas
    
    def calcular_salud_inventario(self, inventario: Inventario) -> int:
        """
        Calcula un score de salud del inventario (0-100).
        
        Args:
            inventario: Inventario a analizar
            
        Returns:
            Score de 0 (crítico) a 100 (óptimo)
        """
        if inventario.esta_agotado:
            return 0
        
        if inventario.cantidad_minima == 0:
            # Sin mínimo configurado, basarse solo en cantidad
            if inventario.cantidad < 10:
                return 30
            elif inventario.cantidad < 50:
                return 60
            return 100
        
        # Calcular ratio contra el mínimo
        ratio = inventario.cantidad / inventario.cantidad_minima
        
        if ratio < 1:
            # Por debajo del mínimo
            return int(ratio * 50)  # 0-50
        elif ratio < 2:
            # Entre 1x y 2x del mínimo
            return int(50 + (ratio - 1) * 30)  # 50-80
        else:
            # Más de 2x el mínimo
            return min(100, int(80 + (ratio - 2) * 5))  # 80-100
