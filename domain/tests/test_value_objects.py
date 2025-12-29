"""
Tests para los Value Objects del dominio
"""
import pytest
from decimal import Decimal

from litethinking_domain.value_objects import (
    NIT, Email, Money, Currency, CodigoProducto, HashBlockchain
)


class TestNIT:
    """Tests para el Value Object NIT."""
    
    def test_nit_valido_con_guion(self):
        """Debe aceptar NIT con guión."""
        nit = NIT("900123456-7")
        assert nit.valor == "900123456-7"
        assert nit.numero_base == "900123456"
        assert nit.digito_verificacion == "7"
    
    def test_nit_valido_sin_guion(self):
        """Debe aceptar NIT sin guión y normalizarlo."""
        nit = NIT("9001234567")
        assert nit.valor == "900123456-7"
    
    def test_nit_vacio_falla(self):
        """Debe fallar con NIT vacío."""
        with pytest.raises(ValueError):
            NIT("")
    
    def test_nit_formato_invalido_falla(self):
        """Debe fallar con formato inválido."""
        with pytest.raises(ValueError):
            NIT("ABC123")
    
    def test_nit_igualdad(self):
        """Debe comparar correctamente dos NITs."""
        nit1 = NIT("900123456-7")
        nit2 = NIT("9001234567")
        nit3 = NIT("900123456-8")
        
        assert nit1 == nit2
        assert nit1 != nit3


class TestEmail:
    """Tests para el Value Object Email."""
    
    def test_email_valido(self):
        """Debe aceptar email válido."""
        email = Email("usuario@ejemplo.com")
        assert email.valor == "usuario@ejemplo.com"
    
    def test_email_normalizado_minusculas(self):
        """Debe normalizar a minúsculas."""
        email = Email("Usuario@Ejemplo.COM")
        assert email.valor == "usuario@ejemplo.com"
    
    def test_email_vacio_falla(self):
        """Debe fallar con email vacío."""
        with pytest.raises(ValueError):
            Email("")
    
    def test_email_formato_invalido_falla(self):
        """Debe fallar con formato inválido."""
        with pytest.raises(ValueError):
            Email("no-es-email")
    
    def test_email_usuario_dominio(self):
        """Debe extraer usuario y dominio correctamente."""
        email = Email("juan@empresa.com")
        assert email.usuario == "juan"
        assert email.dominio == "empresa.com"
    
    def test_email_es_corporativo(self):
        """Debe detectar emails corporativos."""
        email_corp = Email("juan@miempresa.com")
        email_personal = Email("juan@gmail.com")
        
        assert email_corp.es_corporativo is True
        assert email_personal.es_corporativo is False


class TestMoney:
    """Tests para el Value Object Money."""
    
    def test_money_crear_cop(self):
        """Debe crear correctamente dinero en COP."""
        money = Money(1500000, "COP")
        assert money.monto == Decimal("1500000")
        assert money.moneda == Currency.COP
    
    def test_money_crear_usd_decimales(self):
        """Debe manejar decimales en USD."""
        money = Money(99.99, "USD")
        assert money.monto == Decimal("99.99")
    
    def test_money_negativo_falla(self):
        """Debe fallar con monto negativo."""
        with pytest.raises(ValueError):
            Money(-100, "COP")
    
    def test_money_suma(self):
        """Debe sumar correctamente."""
        m1 = Money(100, "USD")
        m2 = Money(50, "USD")
        resultado = m1 + m2
        assert resultado.monto == Decimal("150.00")
    
    def test_money_suma_diferente_moneda_falla(self):
        """Debe fallar al sumar monedas diferentes."""
        m1 = Money(100, "USD")
        m2 = Money(100, "COP")
        with pytest.raises(ValueError):
            m1 + m2
    
    def test_money_multiplicacion(self):
        """Debe multiplicar correctamente."""
        money = Money(100, "USD")
        resultado = money * 3
        assert resultado.monto == Decimal("300.00")
    
    def test_money_formato(self):
        """Debe formatear correctamente."""
        money = Money(1500000, "COP")
        assert "1,500,000" in money.formato() or "1.500.000" in money.formato()


class TestCodigoProducto:
    """Tests para el Value Object CodigoProducto."""
    
    def test_codigo_valido(self):
        """Debe aceptar código válido."""
        codigo = CodigoProducto("PROD-001")
        assert codigo.valor == "PROD-001"
    
    def test_codigo_normalizado_mayusculas(self):
        """Debe normalizar a mayúsculas."""
        codigo = CodigoProducto("prod-001")
        assert codigo.valor == "PROD-001"
    
    def test_codigo_vacio_falla(self):
        """Debe fallar con código vacío."""
        with pytest.raises(ValueError):
            CodigoProducto("")
    
    def test_codigo_muy_corto_falla(self):
        """Debe fallar con código muy corto."""
        with pytest.raises(ValueError):
            CodigoProducto("A")
    
    def test_codigo_caracteres_invalidos_falla(self):
        """Debe fallar con caracteres inválidos."""
        with pytest.raises(ValueError):
            CodigoProducto("PROD@001")
    
    def test_codigo_prefijo(self):
        """Debe extraer el prefijo correctamente."""
        codigo = CodigoProducto("ELEC-001")
        assert codigo.prefijo == "ELEC"


class TestHashBlockchain:
    """Tests para el Value Object HashBlockchain."""
    
    def test_hash_desde_bytes(self):
        """Debe generar hash desde bytes."""
        contenido = b"contenido de prueba"
        hash_obj = HashBlockchain.desde_bytes(contenido)
        assert len(hash_obj.valor) == 64
    
    def test_hash_desde_texto(self):
        """Debe generar hash desde texto."""
        hash_obj = HashBlockchain.desde_texto("texto de prueba")
        assert len(hash_obj.valor) == 64
    
    def test_hash_consistente(self):
        """Debe generar el mismo hash para el mismo contenido."""
        texto = "contenido fijo"
        hash1 = HashBlockchain.desde_texto(texto)
        hash2 = HashBlockchain.desde_texto(texto)
        assert hash1 == hash2
    
    def test_hash_verificar(self):
        """Debe verificar correctamente el contenido."""
        contenido = b"mi documento"
        hash_obj = HashBlockchain.desde_bytes(contenido)
        
        assert hash_obj.verificar(contenido) is True
        assert hash_obj.verificar(b"otro contenido") is False
    
    def test_hash_corto(self):
        """Debe retornar versión corta."""
        hash_obj = HashBlockchain.desde_texto("prueba")
        assert len(hash_obj.corto) == 16
        assert len(hash_obj.muy_corto) == 8
