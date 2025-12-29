from typing import List, Optional
from dataclasses import dataclass

from litethinking_domain.entities import Empresa
from litethinking_domain.value_objects import NIT
from litethinking_domain.exceptions import ValidacionError


@dataclass
class ResultadoValidacion:
    valido: bool
    errores: List[ValidacionError]
    
    @property
    def mensaje(self) -> str:
        if self.valido:
            return "Validación exitosa"
        return "; ".join([e.mensaje for e in self.errores])


class ValidadorEmpresa:
    
    NOMBRE_MIN_LENGTH = 2
    NOMBRE_MAX_LENGTH = 150
    DIRECCION_MIN_LENGTH = 5
    DIRECCION_MAX_LENGTH = 255
    TELEFONO_MIN_LENGTH = 7
    TELEFONO_MAX_LENGTH = 20
    
    def validar(self, empresa: Empresa) -> ResultadoValidacion:
        errores: List[ValidacionError] = []
        
        error_nombre = self._validar_nombre(empresa.nombre)
        if error_nombre:
            errores.append(error_nombre)
        
        error_direccion = self._validar_direccion(empresa.direccion)
        if error_direccion:
            errores.append(error_direccion)
        
        error_telefono = self._validar_telefono(empresa.telefono)
        if error_telefono:
            errores.append(error_telefono)
        
        return ResultadoValidacion(
            valido=len(errores) == 0,
            errores=errores
        )
    
    def _validar_nombre(self, nombre: str) -> Optional[ValidacionError]:
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
        
        caracteres_prohibidos = ["<", ">", "{", "}", "[", "]", "\\"]
        for char in caracteres_prohibidos:
            if char in nombre_limpio:
                return ValidacionError(
                    "nombre",
                    f"El nombre contiene caracteres no permitidos: {char}"
                )
        
        return None
    
    def _validar_direccion(self, direccion: str) -> Optional[ValidacionError]:
        if not direccion or not direccion.strip():
            return ValidacionError("direccion", "La dirección es requerida")
        
        direccion_limpia = direccion.strip()
        
        if len(direccion_limpia) < self.DIRECCION_MIN_LENGTH:
            return ValidacionError(
                "direccion",
                f"La dirección debe tener al menos {self.DIRECCION_MIN_LENGTH} caracteres"
            )
        
        if len(direccion_limpia) > self.DIRECCION_MAX_LENGTH:
            return ValidacionError(
                "direccion",
                f"La dirección no puede exceder {self.DIRECCION_MAX_LENGTH} caracteres"
            )
        
        return None
    
    def _validar_telefono(self, telefono: str) -> Optional[ValidacionError]:
        if not telefono or not telefono.strip():
            return ValidacionError("telefono", "El teléfono es requerido")
        
        telefono_limpio = telefono.strip()
        
        if len(telefono_limpio) < self.TELEFONO_MIN_LENGTH:
            return ValidacionError(
                "telefono",
                f"El teléfono debe tener al menos {self.TELEFONO_MIN_LENGTH} caracteres"
            )
        
        if len(telefono_limpio) > self.TELEFONO_MAX_LENGTH:
            return ValidacionError(
                "telefono",
                f"El teléfono no puede exceder {self.TELEFONO_MAX_LENGTH} caracteres"
            )
        
        caracteres_validos = set("0123456789 +-().")
        for char in telefono_limpio:
            if char not in caracteres_validos:
                return ValidacionError(
                    "telefono",
                    f"El teléfono contiene caracteres inválidos: {char}"
                )
        
        return None
    
    def validar_nit(self, nit_str: str) -> ResultadoValidacion:
        errores = []
        
        try:
            NIT(nit_str)
        except ValueError as e:
            errores.append(ValidacionError("nit", str(e)))
        
        return ResultadoValidacion(
            valido=len(errores) == 0,
            errores=errores
        )
    
    def puede_eliminar(self, empresa: Empresa, tiene_productos: bool) -> ResultadoValidacion:
        errores = []
        
        if tiene_productos:
            errores.append(ValidacionError(
                "empresa",
                "No se puede eliminar una empresa con productos asociados. "
                "Elimine primero los productos."
            ))
        
        return ResultadoValidacion(
            valido=len(errores) == 0,
            errores=errores
        )
