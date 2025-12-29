# 🏛️ Arquitectura del Sistema - Clean Architecture

## 📋 Resumen Ejecutivo

Este proyecto implementa una **Clean Architecture** (Arquitectura Limpia) siguiendo los principios de Robert C. Martin (Uncle Bob), con separación clara entre las capas de:

1. **Dominio** (Domain Layer) - Entidades y reglas de negocio
2. **Aplicación** (Application Layer) - Casos de uso
3. **Infraestructura** (Infrastructure Layer) - Persistencia, APIs, servicios externos
4. **Presentación** (Presentation Layer) - UI React

---

## 🎯 Capa de Dominio (`domain/`)

### Características

- **Independiente de frameworks**: No depende de Django, Flask ni ningún framework
- **Independiente de UI**: No conoce cómo se presenta la información
- **Independiente de bases de datos**: No sabe si usa PostgreSQL, MongoDB o archivos
- **Testeable**: Se puede probar sin infraestructura

### Estructura

```
domain/src/litethinking_domain/
├── entities/                    # Entidades del negocio
│   ├── empresa.py              # Entidad Empresa
│   ├── producto.py             # Entidad Producto
│   ├── inventario.py           # Entidad Inventario
│   └── historial_envio.py      # Entidad HistorialEnvio
│
├── value_objects/               # Objetos de valor inmutables
│   ├── nit.py                  # NIT colombiano validado
│   ├── email.py                # Email validado
│   ├── money.py                # Dinero con moneda
│   ├── codigo_producto.py      # Código de producto
│   └── hash_blockchain.py      # Hash SHA-256
│
├── interfaces/                  # Contratos (Ports)
│   ├── repositories.py         # Interfaces de repositorios
│   └── services.py             # Interfaces de servicios externos
│
├── validators/                  # Reglas de negocio
│   ├── empresa_validator.py
│   ├── producto_validator.py
│   └── inventario_validator.py
│
└── exceptions/                  # Excepciones de dominio
    └── __init__.py
```

### Gestión con Poetry

```toml
# domain/pyproject.toml
[tool.poetry]
name = "litethinking-domain"
version = "1.0.0"
description = "Capa de Dominio - Clean Architecture"

[tool.poetry.dependencies]
python = "^3.10"
pydantic = "^2.5.0"
```

---

## 🔧 Capa de Infraestructura (`backend/`)

### Responsabilidades

- **Persistencia**: Modelos Django ORM
- **API REST**: Django REST Framework
- **Autenticación**: JWT con SimpleJWT
- **Servicios externos**: Resend (email), Gemini (IA)

### Adaptadores

Los adaptadores implementan las interfaces del dominio:

```python
# backend/core/adapters/repositories.py

class DjangoEmpresaRepository(IEmpresaRepository):
    """Implementa la interfaz de dominio usando Django ORM."""
    
    def obtener_por_nit(self, nit: NIT) -> Optional[Empresa]:
        model = EmpresaModel.objects.get(nit=str(nit))
        return EmpresaMapper.to_domain(model)
```

### Mappers

Traducen entre entidades de dominio y modelos Django:

```python
# backend/core/adapters/mappers.py

class EmpresaMapper:
    @staticmethod
    def to_domain(model: EmpresaModel) -> Empresa:
        return Empresa(
            nit=NIT(model.nit),
            nombre=model.nombre,
            direccion=model.direccion,
            telefono=model.telefono
        )
    
    @staticmethod
    def to_model(entity: Empresa) -> EmpresaModel:
        return EmpresaModel(
            nit=str(entity.nit),
            nombre=entity.nombre,
            direccion=entity.direccion,
            telefono=entity.telefono
        )
```

---

## 🎨 Capa de Presentación (`frontend/`)

### Atomic Design

```
frontend/src/components/
├── atoms/          # Elementos básicos (Button, Input, Badge)
├── molecules/      # Combinaciones (FormField, AlertMessage)
├── organisms/      # Secciones completas (NavigationBar, Forms)
└── templates/      # Layouts de página
```

### Servicios API

```javascript
// frontend/src/services/api.js
const API_URL = import.meta.env.VITE_API_URL;

export const empresaService = {
  getAll: () => api.get('/empresas/'),
  create: (data) => api.post('/empresas/', data),
  // ...
};
```

---

## 🔄 Flujo de Datos

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
│   Frontend  │───▶│    API       │───▶│  Adaptador  │───▶│   Dominio    │
│   (React)   │    │  (Django)    │    │  (Mapper)   │    │  (Entidad)   │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
       │                  │                  │                   │
       │                  │                  │                   │
       ▼                  ▼                  ▼                   ▼
   UI/UX            REST API         Traducción         Reglas de
   Components       Endpoints        Entidad↔Modelo     Negocio
```

---

## 📦 Instalación del Paquete de Dominio

### Desarrollo Local

```bash
# 1. Instalar Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 2. Configurar paquete de dominio
cd domain
poetry install

# 3. Instalar en backend (modo editable)
cd ../backend
pip install -e ../domain
```

### Producción (Render)

El archivo `build.sh` se encarga de instalar el paquete:

```bash
# backend/build.sh
if [ -d "../domain" ]; then
    pip install -e ../domain
fi
```

### Publicar en PyPI (Opcional)

```bash
cd domain
poetry build
poetry publish
```

---

## ✅ Principios SOLID Aplicados

| Principio | Aplicación |
|-----------|------------|
| **S**ingle Responsibility | Cada entidad tiene una única responsabilidad |
| **O**pen/Closed | Interfaces permiten extensión sin modificación |
| **L**iskov Substitution | Los repositorios son intercambiables |
| **I**nterface Segregation | Interfaces pequeñas y específicas |
| **D**ependency Inversion | El dominio no depende de infraestructura |

---

## 🧪 Testing

### Tests de Dominio

```bash
cd domain
poetry run pytest -v
```

### Tests de Backend

```bash
cd backend
python manage.py test
```

---

## 📊 Diagrama de Dependencias

```
                    ┌─────────────────┐
                    │    DOMINIO      │
                    │  (Sin deps)     │
                    └────────▲────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
    ┌─────────┴─────────┐    │    ┌─────────┴─────────┐
    │   INFRAESTRUCTURA │    │    │   PRESENTACIÓN    │
    │   (Django, APIs)  │    │    │   (React)         │
    └───────────────────┘    │    └───────────────────┘
                             │
                    ┌────────┴────────┐
                    │   APLICACIÓN    │
                    │  (Casos de uso) │
                    └─────────────────┘
```

> **Nota**: Las flechas apuntan hacia adentro. Las capas externas dependen de las internas, nunca al revés.

---

## 📄 Licencia

MIT License - Lite Thinking 2026
