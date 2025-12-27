# 📦 Inventario Pro | IA + Blockchain

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0+-green?style=for-the-badge&logo=django&logoColor=white)
![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TailwindCSS](https://img.shields.io/badge/Tailwind-3.4+-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)

**Sistema de gestión de inventario empresarial con análisis inteligente (IA) y certificación Blockchain**

[Demo](#-demo) • [Instalación](#-instalación) • [Documentación](#-documentación-api) • [Características](#-características)

</div>

---

## 📋 Descripción

**Inventario Pro** es una aplicación fullstack para la gestión de inventarios empresariales que integra tecnologías modernas como:

- 🤖 **Análisis con IA** - Alertas inteligentes, recomendaciones y resúmenes ejecutivos automáticos
- 🔗 **Certificación Blockchain** - Hash SHA-256 para garantizar integridad de documentos
- 📧 **Envío de correos** - Reportes PDF enviados via Resend API
- 📄 **Generación de PDF** - Reportes profesionales con ReportLab



ENTRE CON EL USUARIO: admins@gmail.com

CONTRASEÑA: 12345678

---

## 🏗️ Arquitectura

```
Django-Project/
├── backend/                 # API REST con Django + DRF
│   ├── api/                 # Endpoints, servicios y lógica
│   │   ├── views.py         # ViewSets y APIViews
│   │   ├── serializers.py   # Serialización de datos
│   │   ├── email_service.py # Generación PDF y envío email
│   │   ├── ia_service.py    # Motor de análisis inteligente
│   │   └── urls.py          # Rutas de la API
│   ├── core/                # Modelos de datos
│   │   └── models/          # Empresa, Producto, Inventario, HistorialEnvio
│   ├── config/              # Configuración Django
│   └── manage.py
│
├── frontend/                # SPA con React + Vite
│   ├── src/
│   │   ├── components/      # Atomic Design (atoms, molecules, organisms)
│   │   ├── pages/           # Páginas de la aplicación
│   │   ├── services/        # Clientes API (axios)
│   │   ├── context/         # AuthContext (JWT)
│   │   └── routes/          # React Router
│   └── index.html
│
└── README.md
```

---

## ✨ Características

### 🏢 Gestión de Empresas

- CRUD completo de empresas (NIT, nombre, dirección, teléfono)
- Búsqueda y filtrado en tiempo real
- Validación de datos

### 📦 Gestión de Productos

- Catálogo de productos por empresa
- Precios multi-moneda (COP, USD, EUR)
- Asociación automática con inventario

### 📊 Gestión de Inventario

- Control de stock por producto
- Actualización de cantidades
- Vista consolidada por empresa

### 🤖 Análisis con IA

- **Alertas inteligentes**: Detecta productos sin stock o con niveles críticos
- **Clasificación automática**: Categoriza por niveles (crítico, bajo, medio, alto)
- **Resumen ejecutivo**: Genera reportes automáticos del estado del inventario
- **Recomendaciones**: Sugiere acciones basadas en el análisis

### 🔗 Certificación Blockchain

- **Hash SHA-256**: Genera huella digital única del documento PDF
- **Hash de contenido**: Certifica el estado exacto del inventario
- **Verificación**: Detecta cualquier alteración del documento

### 📧 Sistema de Correos

- Envío de reportes PDF por email
- Plantillas HTML profesionales
- Integración con Resend API
- Historial de envíos

---

## 🛠️ Tecnologías

### Backend

| Tecnología           | Versión | Descripción       |
| --------------------- | -------- | ------------------ |
| Python                | 3.12+    | Lenguaje principal |
| Django                | 5.0+     | Framework web      |
| Django REST Framework | 3.14+    | API REST           |
| SimpleJWT             | 5.3+     | Autenticación JWT |
| ReportLab             | 4.0+     | Generación de PDF |
| Resend                | 2.0+     | Envío de emails   |
| SQLite/PostgreSQL     | -        | Base de datos      |

### Frontend

| Tecnología  | Versión | Descripción   |
| ------------ | -------- | -------------- |
| React        | 18+      | Librería UI   |
| Vite         | 5+       | Build tool     |
| TailwindCSS  | 3.4+     | Estilos        |
| Axios        | 1.6+     | Cliente HTTP   |
| React Router | 6+       | Enrutamiento   |
| jsPDF        | 2.5+     | PDF en cliente |

---

## 📋 Requisitos Previos

- **Python** 3.12 o superior
- **Node.js** 18 o superior
- **npm** o **yarn**
- **Git**

---

## 🚀 Instalación

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/Django-Project.git
cd Django-Project
```

### 2️⃣ Configurar Backend (Django)

```bash
# Entrar al directorio backend
cd backend

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En macOS/Linux:
source .venv/bin/activate
# En Windows:
.venv\Scripts\activate

# Instalar dependencias
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers
pip install reportlab resend python-dotenv pillow qrcode

# Crear archivo de variables de entorno
cp .env.example .env
# Editar .env con tus credenciales (ver sección Variables de Entorno)

# Aplicar migraciones
python manage.py migrate

# Crear superusuario (admin)
python manage.py createsuperuser

# Iniciar servidor de desarrollo
python manage.py runserver 8001
```

### 3️⃣ Configurar Frontend (React)

```bash
# En otra terminal, desde la raíz del proyecto
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

### 4️⃣ Acceder a la aplicación

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8001/api/
- **Admin Django**: http://localhost:8001/admin/

---

## 🔐 Variables de Entorno

Crear archivo `backend/.env` con las siguientes variables:

```env
# Django
SECRET_KEY=tu-secret-key-muy-segura
DEBUG=True

# Email - Resend API (https://resend.com)
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxxxxxxx
EMAIL_FROM=onboarding@resend.dev

# IA Avanzada (Opcional)
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
```

> 💡 **Nota**: Para obtener una API key de Resend, regístrate en [resend.com](https://resend.com). La cuenta gratuita permite enviar desde `onboarding@resend.dev`.

---

## 📖 Documentación API

### Autenticación

| Método | Endpoint               | Descripción             |
| ------- | ---------------------- | ------------------------ |
| POST    | `/api/auth/login/`   | Obtener tokens JWT       |
| POST    | `/api/auth/refresh/` | Refrescar access token   |
| GET     | `/api/auth/me/`      | Información del usuario |

**Ejemplo login:**

```bash
curl -X POST http://localhost:8001/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "tu-password"}'
```

### Empresas

| Método | Endpoint                 | Descripción       | Auth  |
| ------- | ------------------------ | ------------------ | ----- |
| GET     | `/api/empresas/`       | Listar empresas    | No    |
| POST    | `/api/empresas/`       | Crear empresa      | Admin |
| GET     | `/api/empresas/{nit}/` | Detalle empresa    | No    |
| PUT     | `/api/empresas/{nit}/` | Actualizar empresa | Admin |
| DELETE  | `/api/empresas/{nit}/` | Eliminar empresa   | Admin |

### Productos

| Método | Endpoint                          | Descripción          | Auth  |
| ------- | --------------------------------- | --------------------- | ----- |
| GET     | `/api/productos/`               | Listar productos      | No    |
| GET     | `/api/productos/?empresa={nit}` | Productos por empresa | No    |
| POST    | `/api/productos/`               | Crear producto        | Admin |
| PUT     | `/api/productos/{id}/`          | Actualizar producto   | Admin |
| DELETE  | `/api/productos/{id}/`          | Eliminar producto     | Admin |

### Inventario

| Método | Endpoint                             | Descripción           | Auth  |
| ------- | ------------------------------------ | ---------------------- | ----- |
| GET     | `/api/inventarios/`                | Listar inventarios     | Sí   |
| GET     | `/api/inventarios/?empresa={nit}`  | Inventario por empresa | Sí   |
| PATCH   | `/api/inventarios/{id}/`           | Actualizar cantidad    | Admin |
| GET     | `/api/inventarios/pdf/{nit}/`      | Descargar PDF          | Sí   |
| POST    | `/api/inventarios/enviar-correo/`  | Enviar por email       | Sí   |
| GET     | `/api/inventarios/analisis/{nit}/` | Análisis IA           | Sí   |

### Historial de Envíos

| Método | Endpoint                                 | Descripción        | Auth |
| ------- | ---------------------------------------- | ------------------- | ---- |
| GET     | `/api/historial-envios/`               | Listar envíos      | Sí  |
| GET     | `/api/historial-envios/?empresa={nit}` | Envíos por empresa | Sí  |

---

## 📧 Envío de Correos

### Request

```bash
curl -X POST http://localhost:8001/api/inventarios/enviar-correo/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "empresa_nit": "123456789-0",
    "email_destino": "cliente@ejemplo.com",
    "incluir_analisis_ia": true,
    "incluir_blockchain": true
  }'
```

### Response

```json
{
  "success": true,
  "message": "Correo enviado exitosamente a cliente@ejemplo.com",
  "provider": "resend",
  "historial_id": 1,
  "hash_documento": "a7b9c3d8e2f1...",
  "alertas_count": 2
}
```

---

## 🖼️ Screenshots

### Landing Page

Vista principal con información del sistema y accesos rápidos.

### Gestión de Inventario

Panel con listado de empresas, productos y opciones de exportación.

### Modal de Envío de Correo

Opciones para incluir análisis IA y certificación Blockchain.

### Página IA Beta

Documentación interactiva de las funcionalidades de IA y Blockchain.

---

## 🧪 Testing

### Backend

```bash
cd backend
python manage.py test
```

### Frontend

```bash
cd frontend
npm run lint
```

---

## 📁 Estructura de Componentes (Atomic Design)

```
frontend/src/components/
├── atoms/           # Componentes básicos
│   ├── Button.jsx
│   ├── Input.jsx
│   ├── Modal.jsx
│   ├── Badge.jsx
│   └── Spinner.jsx
├── molecules/       # Combinaciones de atoms
│   ├── FormField.jsx
│   ├── AlertMessage.jsx
│   ├── ConfirmDialog.jsx
│   └── DataTable.jsx
├── organisms/       # Secciones completas
│   ├── NavigationBar.jsx
│   ├── EmpresaForm.jsx
│   ├── ProductoForm.jsx
│   └── InventarioForm.jsx
└── templates/       # Layouts de página
    ├── AuthTemplate.jsx
    └── LandingTemplate.jsx
```

---

## 🤝 Contribución

1. Fork el proyecto
2. Crea tu rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👨‍💻 Autor

**Juan David Amézquita Núñez**

---

<div align="center">

Hecho con ❤️ usando Django + React

</div>
