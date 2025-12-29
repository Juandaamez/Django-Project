class DomainException(Exception):
    """Excepción base para todos los errores de dominio."""
    
    def __init__(self, mensaje: str, codigo: str = "DOMAIN_ERROR"):
        self.mensaje = mensaje
        self.codigo = codigo
        super().__init__(mensaje)
    
    def to_dict(self) -> dict:
        """Convierte la excepción a diccionario para APIs."""
        return {
            "error": True,
            "codigo": self.codigo,
            "mensaje": self.mensaje
        }


# ═══════════════════════════════════════════════════════════════
# Excepciones de Empresa
# ═══════════════════════════════════════════════════════════════

class EmpresaNoEncontradaError(DomainException):
    """La empresa solicitada no existe."""
    
    def __init__(self, nit: str):
        super().__init__(
            f"No se encontró la empresa con NIT: {nit}",
            "EMPRESA_NO_ENCONTRADA"
        )
        self.nit = nit


class EmpresaYaExisteError(DomainException):
    """Ya existe una empresa con el NIT dado."""
    
    def __init__(self, nit: str):
        super().__init__(
            f"Ya existe una empresa con NIT: {nit}",
            "EMPRESA_DUPLICADA"
        )
        self.nit = nit


class EmpresaInactivaError(DomainException):
    """La empresa está inactiva y no puede realizar operaciones."""
    
    def __init__(self, nit: str):
        super().__init__(
            f"La empresa con NIT {nit} está inactiva",
            "EMPRESA_INACTIVA"
        )
        self.nit = nit


# ═══════════════════════════════════════════════════════════════
# Excepciones de Producto
# ═══════════════════════════════════════════════════════════════

class ProductoNoEncontradoError(DomainException):
    """El producto solicitado no existe."""
    
    def __init__(self, codigo: str):
        super().__init__(
            f"No se encontró el producto con código: {codigo}",
            "PRODUCTO_NO_ENCONTRADO"
        )
        self.codigo = codigo


class ProductoYaExisteError(DomainException):
    """Ya existe un producto con el código dado."""
    
    def __init__(self, codigo: str):
        super().__init__(
            f"Ya existe un producto con código: {codigo}",
            "PRODUCTO_DUPLICADO"
        )
        self.codigo = codigo


class ProductoSinPrecioError(DomainException):
    """El producto no tiene precio en la moneda solicitada."""
    
    def __init__(self, codigo: str, moneda: str):
        super().__init__(
            f"El producto {codigo} no tiene precio en {moneda}",
            "PRODUCTO_SIN_PRECIO"
        )
        self.codigo = codigo
        self.moneda = moneda


# ═══════════════════════════════════════════════════════════════
# Excepciones de Inventario
# ═══════════════════════════════════════════════════════════════

class InventarioNoEncontradoError(DomainException):
    """El registro de inventario no existe."""
    
    def __init__(self, identificador: str):
        super().__init__(
            f"No se encontró el inventario: {identificador}",
            "INVENTARIO_NO_ENCONTRADO"
        )


class StockInsuficienteError(DomainException):
    """No hay suficiente stock para la operación."""
    
    def __init__(self, producto_codigo: str, disponible: int, solicitado: int):
        super().__init__(
            f"Stock insuficiente para {producto_codigo}. "
            f"Disponible: {disponible}, Solicitado: {solicitado}",
            "STOCK_INSUFICIENTE"
        )
        self.producto_codigo = producto_codigo
        self.disponible = disponible
        self.solicitado = solicitado


class CantidadInvalidaError(DomainException):
    """La cantidad especificada no es válida."""
    
    def __init__(self, cantidad: int, razon: str = ""):
        mensaje = f"Cantidad inválida: {cantidad}"
        if razon:
            mensaje += f". {razon}"
        super().__init__(mensaje, "CANTIDAD_INVALIDA")
        self.cantidad = cantidad


# ═══════════════════════════════════════════════════════════════
# Excepciones de Envío
# ═══════════════════════════════════════════════════════════════

class EnvioFallidoError(DomainException):
    """El envío de correo falló."""
    
    def __init__(self, email: str, razon: str):
        super().__init__(
            f"Fallo al enviar email a {email}: {razon}",
            "ENVIO_FALLIDO"
        )
        self.email = email
        self.razon = razon


class ServicioNoDisponibleError(DomainException):
    """Un servicio externo no está disponible."""
    
    def __init__(self, servicio: str, detalle: str = ""):
        mensaje = f"Servicio no disponible: {servicio}"
        if detalle:
            mensaje += f". {detalle}"
        super().__init__(mensaje, "SERVICIO_NO_DISPONIBLE")
        self.servicio = servicio


# ═══════════════════════════════════════════════════════════════
# Excepciones de Validación
# ═══════════════════════════════════════════════════════════════

class ValidacionError(DomainException):
    """Error de validación de datos."""
    
    def __init__(self, campo: str, mensaje: str):
        super().__init__(
            f"Error de validación en {campo}: {mensaje}",
            "VALIDACION_ERROR"
        )
        self.campo = campo
    
    def to_dict(self) -> dict:
        base = super().to_dict()
        base["campo"] = self.campo
        return base


class MultipleValidacionError(DomainException):
    """Múltiples errores de validación."""
    
    def __init__(self, errores: list):
        self.errores = errores
        mensaje = "; ".join([f"{e.campo}: {e.mensaje}" for e in errores])
        super().__init__(mensaje, "VALIDACION_MULTIPLE")
    
    def to_dict(self) -> dict:
        return {
            "error": True,
            "codigo": self.codigo,
            "mensaje": self.mensaje,
            "errores": [e.to_dict() for e in self.errores]
        }


# ═══════════════════════════════════════════════════════════════
# Excepciones de Autorización
# ═══════════════════════════════════════════════════════════════

class AccesoDenegadoError(DomainException):
    """El usuario no tiene permiso para esta operación."""
    
    def __init__(self, operacion: str, razon: str = ""):
        mensaje = f"Acceso denegado para: {operacion}"
        if razon:
            mensaje += f". {razon}"
        super().__init__(mensaje, "ACCESO_DENEGADO")
        self.operacion = operacion


class UsuarioNoAutenticadoError(DomainException):
    """Se requiere autenticación para esta operación."""
    
    def __init__(self):
        super().__init__(
            "Se requiere autenticación para esta operación",
            "NO_AUTENTICADO"
        )
