# Lite Thinking Domain Layer

## 📋 Descripción

Este paquete contiene la **Capa de Dominio** del sistema de inventario Lite Thinking, implementado siguiendo los principios de **Clean Architecture** y **Domain-Driven Design (DDD)**.

La capa de dominio es completamente **independiente** de:

- Frameworks web (Django, FastAPI, etc.)
- ORMs y bases de datos
- APIs HTTP/REST
- Interfaces de usuario

## 🏗️ Arquitectura

```
domain/
├── src/
│   └── litethinking_domain/
│       ├── entities/          # Entidades del negocio
│       │   ├── empresa.py
│       │   ├── producto.py
│       │   ├── inventario.py
│       │   └── historial_envio.py
│       ├── value_objects/     # Objetos de valor inmutables
│       │   ├── nit.py
│       │   ├── email.py
│       │   ├── money.py
│       │   └── hash_blockchain.py
│       ├── interfaces/        # Contratos/Interfaces (Ports)
│       │   ├── repositories/
│       │   └── services/
│       ├── exceptions/        # Excepciones de dominio
│       └── validators/        # Validadores de reglas de negocio
├── tests/
├── pyproject.toml
└── README.md
```

## 📦 Instalación

### Desarrollo local (editable)

```bash
cd domain
poetry install
```

### Desde el Backend

```bash
cd backend
pip install -e ../domain
# o con poetry
poetry add ../domain
```

### Publicar en PyPI (producción)

```bash
poetry build
poetry publish
```

## 🧪 Testing

```bash
cd domain
poetry run pytest
```

## 📖 Uso

```python
from litethinking_domain.entities import Empresa, Producto, Inventario
from litethinking_domain.value_objects import NIT, Email, Money
from litethinking_domain.validators import ValidadorEmpresa

# Crear una entidad de dominio
empresa = Empresa(
    nit=NIT("900123456-7"),
    nombre="Mi Empresa S.A.S",
    direccion="Calle 123 #45-67",
    telefono="+57 300 1234567"
)

# Validar reglas de negocio
validador = ValidadorEmpresa()
errores = validador.validar(empresa)
if errores:
    raise ValueError(f"Empresa inválida: {errores}")

# Crear productos con precios en múltiples monedas
producto = Producto(
    codigo="PROD-001",
    nombre="Laptop",
    caracteristicas="Intel i7, 16GB RAM, 512GB SSD",
    precios={
        "COP": Money(3500000, "COP"),
        "USD": Money(900, "USD"),
    },
    empresa_nit=empresa.nit
)
```

## 🔒 Principios Aplicados

- **Single Responsibility**: Cada entidad tiene una única responsabilidad
- **Open/Closed**: Extensible sin modificar código existente
- **Liskov Substitution**: Interfaces bien definidas
- **Interface Segregation**: Interfaces pequeñas y específicas
- **Dependency Inversion**: Dependencias hacia abstracciones
