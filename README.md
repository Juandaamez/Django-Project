# Inventario Pro

Demo fullstack para gestion de inventario empresarial con Django REST, React,
JWT, reportes PDF, historial de envios, analisis inteligente de stock y
certificacion de documentos mediante hashes SHA-256.

El objetivo del proyecto es mostrar una aplicacion de portafolio que se pueda
probar de punta a punta: iniciar sesion, consultar empresas, gestionar
productos, revisar inventario, generar reportes y ver alertas operativas.

## Demo rapido

Credenciales sembradas por `python manage.py seed_demo`:

| Rol | Email | Password |
| --- | --- | --- |
| Admin | `admin.demo@example.com` | `DemoAdmin2026!` |
| Lectura | `demo@example.com` | `DemoUser2026!` |

Flujo recomendado para evaluar el demo:

1. Entrar al frontend.
2. Iniciar sesion como admin.
3. Abrir Empresas y expandir una empresa para ver productos.
4. Abrir Inventario y revisar productos con stock critico, bajo y saludable.
5. Descargar PDF del inventario.
6. Enviar reporte: en `DEMO_MODE=True` el envio se simula si no hay Resend.
7. Revisar el analisis inteligente y los hashes del reporte.

## Stack

| Capa | Tecnologias |
| --- | --- |
| Frontend | React, Vite, React Router, TailwindCSS, Axios |
| Backend | Django, Django REST Framework, SimpleJWT, drf-spectacular |
| Dominio | Paquete Python local `litethinking-domain` con modelos Django ORM |
| Reportes | ReportLab, generacion PDF, hashes SHA-256 |
| Integraciones | Resend opcional para correo, proveedores IA opcionales |
| Deploy | Render para API, Vercel para frontend |

## Arquitectura

```text
Django-Project/
  backend/    API REST, auth, servicios, reportes, comandos de demo
  domain/     paquete instalable con modelos de negocio Django ORM
  frontend/   aplicacion React con componentes Atomic Design
```

El paquete `domain` funciona como fuente compartida de modelos de negocio. El
backend lo instala como dependencia local y expone los casos de uso mediante
DRF. La UI consume esos endpoints con servicios Axios y maneja sesion con JWT.

## Funcionalidades

- CRUD de empresas, productos e inventario.
- Login con JWT y roles admin/lectura.
- Busqueda y filtros por empresa, producto y NIT.
- Reporte PDF descargable por empresa.
- Envio de reporte por correo con historial.
- Modo demo sin dependencias externas de email.
- Analisis de inventario por reglas: agotado, stock bajo, saludable y valor.
- Hash SHA-256 del PDF y del contenido del inventario.
- Documentacion OpenAPI en `/api/docs/`.

## Instalacion local

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e ../domain
copy .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 8001
```

API local:

- Base URL: `http://localhost:8001/api`
- Swagger: `http://localhost:8001/api/docs/`
- Admin Django: `http://localhost:8001/admin/`

### Frontend

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

Frontend local: `http://localhost:5173`

## Variables de entorno

Backend minimo:

```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
FRONTEND_URL=http://localhost:5173
DEMO_MODE=True
```

Frontend minimo:

```env
VITE_API_URL=http://localhost:8001/api
```

Para envio real de correos:

```env
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxx
EMAIL_FROM=Inventario Pro <onboarding@resend.dev>
```

## Comandos utiles

```bash
# Backend
python manage.py test
python manage.py seed_demo --reset
python manage.py spectacular --file schema.yml

# Frontend
npm run lint
npm run build
```

## Deploy

El backend incluye `render.yaml` para Render. En un despliegue demo se puede
usar:

```env
DEMO_MODE=true
SEED_DEMO_DATA=true
FRONTEND_URL=https://tu-frontend.vercel.app
```

El frontend incluye `frontend/vercel.json` para servir rutas SPA en Vercel.
Configura `VITE_API_URL` con la URL publica del backend.

## Lo que demuestra este proyecto

- Separacion clara entre UI, API y paquete de dominio.
- Manejo de autenticacion JWT y permisos por rol.
- Integracion frontend-backend con servicios reutilizables.
- Generacion de documentos y trazabilidad por hash.
- Pruebas backend sobre serializers, endpoints y servicios.
- Preparacion para deploy real con modo demo reproducible.
