# Lite Thinking Domain Layer

## 📋 Descripción

Este paquete contiene la **Capa de Dominio** del sistema de inventario Lite Thinking, implementado siguiendo los principios de **Clean Architecture**.

La capa de dominio contiene **TODOS los modelos Django** del negocio y es la **única fuente de verdad** para las entidades del sistema.

## 🔑 Características

- ✅ Modelos Django (ORM) para persistencia
- ✅ Gestionado con Poetry
- ✅ Instalable como paquete Python
- ✅ Migraciones Django incluidas
- ✅ Compatible con Django 5.0 - 6.x

## 🏗️ Arquitectura

```
domain/
├── src/
│   └── litethinking_domain/
│       ├── __init__.py        # Configuración de la app Django
│       ├── apps.py            # AppConfig
│       ├── models/            # Modelos Django ORM
│       │   ├── __init__.py
│       │   ├── empresa.py     # Modelo Empresa
│       │   ├── producto.py    # Modelo Producto
│       │   ├── inventario.py  # Modelo Inventario
│       │   └── historial_envio.py  # Modelo HistorialEnvio
│       └── migrations/        # Migraciones Django
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
```

## 🎯 Uso

### En settings.py

```python
INSTALLED_APPS = [
    # ... otras apps
    'litethinking_domain',  # Capa de Dominio (modelos)
    # ... apps que usan los modelos
]
```

### Importar Modelos

```python
from litethinking_domain.models import Empresa, Producto, Inventario, HistorialEnvio

# Uso normal de Django ORM
empresa = Empresa.objects.create(
    nit="123456789",
    nombre="Mi Empresa",
    direccion="Calle 123",
    telefono="555-1234"
)

productos = Producto.objects.filter(empresa=empresa)
```

## 📊 Modelos

### Empresa
- **nit** (PK): Número de Identificación Tributaria
- **nombre**: Nombre de la empresa
- **direccion**: Dirección física
- **telefono**: Teléfono de contacto

### Producto
- **codigo** (unique): Código del producto
- **nombre**: Nombre del producto
- **caracteristicas**: Descripción
- **precios**: JSONField con precios por moneda
- **empresa** (FK): Empresa propietaria

### Inventario
- **producto** (FK): Producto asociado
- **cantidad**: Stock disponible
- **fecha_actualizacion**: Auto-actualizado

### HistorialEnvio
- Registro de envíos de reportes por correo
- Certificación blockchain con hash SHA-256
- Integración con análisis de IA

## 🔧 Migraciones

```bash
# Crear migraciones
python manage.py makemigrations litethinking_domain

# Aplicar migraciones
python manage.py migrate litethinking_domain
```

## 📄 Licencia

MIT License

