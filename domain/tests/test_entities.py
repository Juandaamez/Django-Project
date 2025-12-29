import pytest
from datetime import datetime
from decimal import Decimal

from litethinking_domain.entities import Empresa, Producto, Inventario
from litethinking_domain.value_objects import NIT, CodigoProducto, Money


class TestEmpresa:
    
    def test_crear_empresa_valida(self):
        """Debe crear una empresa con datos válidos."""
        nit = NIT("900123456-7")
        empresa = Empresa(
            nit=nit,
            nombre="Mi Empresa S.A.S",
            direccion="Calle 123 #45-67",
            telefono="+57 300 1234567"
        )
        
        assert empresa.nit == nit
        assert empresa.nombre == "Mi Empresa S.A.S"
        assert empresa.activa is True
    
    def test_empresa_nombre_vacio_falla(self):
        """Debe fallar si el nombre está vacío."""
        with pytest.raises(ValueError, match="nombre"):
            Empresa(
                nit=NIT("900123456-7"),
                nombre="",
                direccion="Calle 123",
                telefono="1234567"
            )
    
    def test_empresa_direccion_corta_falla(self):
        """Debe fallar si la dirección es muy corta."""
        with pytest.raises(ValueError, match="dirección"):
            Empresa(
                nit=NIT("900123456-7"),
                nombre="Empresa Test",
                direccion="Ca",
                telefono="1234567"
            )
    
    def test_empresa_actualizar_datos(self):
        """Debe crear una nueva instancia con datos actualizados."""
        empresa = Empresa(
            nit=NIT("900123456-7"),
            nombre="Empresa Original",
            direccion="Dirección Original",
            telefono="1234567"
        )
        
        empresa_actualizada = empresa.actualizar_datos(
            nombre="Empresa Actualizada"
        )
        
        assert empresa_actualizada.nombre == "Empresa Actualizada"
        assert empresa_actualizada.direccion == empresa.direccion
        assert empresa.nombre == "Empresa Original"  # Inmutabilidad
    
    def test_empresa_desactivar(self):
        """Debe desactivar correctamente una empresa."""
        empresa = Empresa(
            nit=NIT("900123456-7"),
            nombre="Empresa Test",
            direccion="Dirección Test",
            telefono="1234567"
        )
        
        empresa_inactiva = empresa.desactivar()
        
        assert empresa_inactiva.activa is False
        assert empresa.activa is True  # Inmutabilidad


class TestProducto:
    """Tests para la entidad Producto."""
    
    def test_crear_producto_valido(self):
        """Debe crear un producto con datos válidos."""
        producto = Producto(
            codigo=CodigoProducto("PROD-001"),
            nombre="Laptop HP",
            caracteristicas="Intel i7, 16GB RAM",
            precios={"COP": Money(3500000, "COP")},
            empresa_nit=NIT("900123456-7")
        )
        
        assert str(producto.codigo) == "PROD-001"
        assert producto.nombre == "Laptop HP"
    
    def test_producto_sin_precios_falla(self):
        """Debe fallar si no tiene precios."""
        with pytest.raises(ValueError, match="precio"):
            Producto(
                codigo=CodigoProducto("PROD-001"),
                nombre="Producto Test",
                caracteristicas="",
                precios={},
                empresa_nit=NIT("900123456-7")
            )
    
    def test_producto_obtener_precio(self):
        """Debe obtener el precio en la moneda especificada."""
        producto = Producto(
            codigo=CodigoProducto("PROD-001"),
            nombre="Laptop",
            caracteristicas="",
            precios={
                "COP": Money(3500000, "COP"),
                "USD": Money(900, "USD")
            },
            empresa_nit=NIT("900123456-7")
        )
        
        precio_cop = producto.obtener_precio("COP")
        precio_usd = producto.obtener_precio("USD")
        precio_eur = producto.obtener_precio("EUR")
        
        assert precio_cop is not None
        assert precio_cop.monto == Decimal("3500000")
        assert precio_usd is not None
        assert precio_eur is None


class TestInventario:
    """Tests para la entidad Inventario."""
    
    def test_crear_inventario_valido(self):
        """Debe crear un inventario con datos válidos."""
        inventario = Inventario(
            id=1,
            producto_codigo=CodigoProducto("PROD-001"),
            cantidad=100,
            cantidad_minima=10
        )
        
        assert inventario.cantidad == 100
        assert inventario.requiere_reposicion is False
    
    def test_inventario_cantidad_negativa_falla(self):
        """Debe fallar con cantidad negativa."""
        with pytest.raises(ValueError, match="negativa"):
            Inventario(
                id=1,
                producto_codigo=CodigoProducto("PROD-001"),
                cantidad=-5
            )
    
    def test_inventario_agregar_stock(self):
        """Debe agregar stock correctamente."""
        inventario = Inventario(
            id=1,
            producto_codigo=CodigoProducto("PROD-001"),
            cantidad=100
        )
        
        inventario_actualizado = inventario.agregar_stock(50)
        
        assert inventario_actualizado.cantidad == 150
        assert inventario.cantidad == 100  # Inmutabilidad
    
    def test_inventario_reducir_stock(self):
        """Debe reducir stock correctamente."""
        inventario = Inventario(
            id=1,
            producto_codigo=CodigoProducto("PROD-001"),
            cantidad=100
        )
        
        inventario_actualizado = inventario.reducir_stock(30)
        
        assert inventario_actualizado.cantidad == 70
    
    def test_inventario_reducir_stock_insuficiente_falla(self):
        """Debe fallar si no hay suficiente stock."""
        inventario = Inventario(
            id=1,
            producto_codigo=CodigoProducto("PROD-001"),
            cantidad=10
        )
        
        with pytest.raises(ValueError, match="insuficiente"):
            inventario.reducir_stock(20)
    
    def test_inventario_requiere_reposicion(self):
        """Debe detectar cuando requiere reposición."""
        inventario = Inventario(
            id=1,
            producto_codigo=CodigoProducto("PROD-001"),
            cantidad=5,
            cantidad_minima=10
        )
        
        assert inventario.requiere_reposicion is True
        assert inventario.esta_agotado is False
    
    def test_inventario_agotado(self):
        """Debe detectar cuando está agotado."""
        inventario = Inventario(
            id=1,
            producto_codigo=CodigoProducto("PROD-001"),
            cantidad=0
        )
        
        assert inventario.esta_agotado is True
