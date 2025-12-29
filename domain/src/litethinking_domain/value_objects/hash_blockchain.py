"""
Value Object: HashBlockchain
============================

Objeto de valor inmutable que representa un hash SHA-256 
para certificación blockchain de documentos.
"""

from dataclasses import dataclass
import hashlib
import json
from typing import Union, List, Dict, Any


@dataclass(frozen=True)
class HashBlockchain:
    """
    Hash SHA-256 para verificación de autenticidad.
    
    Se utiliza para certificar documentos y contenido,
    simulando un registro blockchain inmutable.
    
    Ejemplo:
        hash = HashBlockchain.desde_bytes(pdf_bytes)
        hash = HashBlockchain.desde_texto("contenido a hashear")
    """
    valor: str
    
    def __post_init__(self) -> None:
        """Valida el formato del hash."""
        if not self.valor:
            raise ValueError("El hash no puede estar vacío")
        
        # Normalizar a minúsculas
        valor_limpio = self.valor.strip().lower()
        
        # Validar formato hexadecimal de 64 caracteres (SHA-256)
        if len(valor_limpio) != 64:
            raise ValueError(f"Hash SHA-256 debe tener 64 caracteres, tiene {len(valor_limpio)}")
        
        try:
            int(valor_limpio, 16)
        except ValueError:
            raise ValueError("Hash debe ser un string hexadecimal válido")
        
        object.__setattr__(self, 'valor', valor_limpio)
    
    @classmethod
    def desde_bytes(cls, contenido: bytes) -> "HashBlockchain":
        """
        Genera un hash desde contenido en bytes.
        
        Args:
            contenido: Bytes a hashear (ej: contenido de un PDF)
        """
        if not contenido:
            raise ValueError("El contenido no puede estar vacío")
        
        hash_valor = hashlib.sha256(contenido).hexdigest()
        return cls(hash_valor)
    
    @classmethod
    def desde_texto(cls, texto: str, encoding: str = "utf-8") -> "HashBlockchain":
        """
        Genera un hash desde texto.
        
        Args:
            texto: Texto a hashear
            encoding: Codificación del texto
        """
        if not texto:
            raise ValueError("El texto no puede estar vacío")
        
        contenido_bytes = texto.encode(encoding)
        return cls.desde_bytes(contenido_bytes)
    
    @classmethod
    def desde_json(cls, datos: Union[Dict[str, Any], List[Any]]) -> "HashBlockchain":
        """
        Genera un hash desde datos JSON.
        Ordena las claves para garantizar consistencia.
        
        Args:
            datos: Diccionario o lista a hashear
        """
        if not datos:
            raise ValueError("Los datos no pueden estar vacíos")
        
        # Serializar con claves ordenadas para consistencia
        json_str = json.dumps(datos, sort_keys=True, ensure_ascii=False)
        return cls.desde_texto(json_str)
    
    @classmethod
    def desde_inventario(cls, inventarios: List[Dict[str, Any]]) -> "HashBlockchain":
        """
        Genera un hash del contenido del inventario para blockchain.
        
        Args:
            inventarios: Lista de items del inventario
        """
        # Crear representación canónica del inventario
        datos = []
        for inv in inventarios:
            datos.append({
                'codigo': inv.get('producto_codigo', inv.get('codigo', '')),
                'nombre': inv.get('producto_nombre', inv.get('nombre', '')),
                'cantidad': inv.get('cantidad', 0),
            })
        
        # Ordenar para consistencia
        datos.sort(key=lambda x: x['codigo'])
        
        return cls.desde_json(datos)
    
    @property
    def corto(self) -> str:
        """Retorna una versión corta del hash (primeros 16 caracteres)."""
        return self.valor[:16]
    
    @property
    def muy_corto(self) -> str:
        """Retorna una versión muy corta del hash (primeros 8 caracteres)."""
        return self.valor[:8]
    
    def verificar(self, contenido: bytes) -> bool:
        """
        Verifica si el contenido coincide con este hash.
        
        Args:
            contenido: Bytes a verificar
            
        Returns:
            True si el hash del contenido coincide
        """
        hash_contenido = hashlib.sha256(contenido).hexdigest()
        return self.valor == hash_contenido
    
    def __str__(self) -> str:
        return self.valor
    
    def __repr__(self) -> str:
        return f"HashBlockchain({self.corto}...)"
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, HashBlockchain):
            return self.valor == other.valor
        if isinstance(other, str):
            return self.valor == other.lower()
        return False
    
    def __hash__(self) -> int:
        return hash(self.valor)
