# 📧 Configuración de Envío de Correos - Lite Thinking

Este documento describe cómo configurar y utilizar la funcionalidad de envío de correos del sistema de inventario.

## 🚀 Resumen de Funcionalidades

El sistema de inventario incluye las siguientes funcionalidades avanzadas para el envío de reportes por correo:

### ✅ Funcionalidades Implementadas

1. **Generación de PDF Profesional**
   - Diseño minimalista y elegante
   - Estadísticas visuales del inventario
   - Tabla de productos con estados de stock
   - Header y footer corporativos

2. **Envío de Correos via API REST**
   - Integración con Resend API (recomendado)
   - Fallback a Django SMTP
   - Correo HTML responsivo y moderno

3. **🤖 Análisis Inteligente (IA)**
   - Alertas automáticas de stock bajo/agotado
   - Recomendaciones de reabastecimiento
   - Resumen ejecutivo del inventario
   - Clasificación por niveles de stock

4. **⛓️ Certificación Blockchain**
   - Hash SHA-256 del documento PDF
   - Hash del contenido del inventario
   - Verificación de autenticidad
   - Código QR de verificación (requiere `qrcode` instalado)

5. **📊 Historial de Envíos**
   - Registro de todos los correos enviados
   - Estado del envío (enviado/fallido/pendiente)
   - Almacenamiento de alertas IA y hashes
   - Consulta por empresa

---

## ⚙️ Configuración

### Opción 1: Resend API (Recomendado)

[Resend](https://resend.com) es un servicio moderno de email con API REST, plan gratuito de 3,000 emails/mes.

1. **Crear cuenta en Resend:**
   ```
   https://resend.com/signup
   ```

2. **Obtener API Key:**
   - Ir a Dashboard > API Keys
   - Crear nueva API Key
   - Copiar la key (empieza con `re_`)

3. **Configurar variable de entorno:**
   ```bash
   export RESEND_API_KEY='re_tu_api_key_aqui'
   ```

   O agregar en `backend/config/settings.py`:
   ```python
   RESEND_API_KEY = 're_tu_api_key_aqui'
   ```

4. **Configurar remitente (opcional):**
   ```bash
   export EMAIL_FROM='Inventario <onboarding@resend.dev>'
   ```

   > **Nota:** El dominio `onboarding@resend.dev` funciona para pruebas. Para producción, verifica tu propio dominio en Resend.

### Opción 2: Django SMTP (Gmail, Outlook, etc.)

Si prefieres usar SMTP tradicional:

1. **Para Gmail:**
   ```python
   # settings.py
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'tu-correo@gmail.com'
   EMAIL_HOST_PASSWORD = 'tu-app-password'  # NO tu contraseña normal
   ```

   > **Importante:** Debes generar una "Contraseña de aplicación" en Google:
   > Cuenta Google > Seguridad > Verificación en 2 pasos > Contraseñas de aplicación

2. **Para Outlook/Office365:**
   ```python
   EMAIL_HOST = 'smtp.office365.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'tu-correo@outlook.com'
   EMAIL_HOST_PASSWORD = 'tu-password'
   ```

---

## 🔧 Instalación de Dependencias Opcionales

### Código QR (Opcional)
```bash
pip install qrcode[pil]
```

### IA Avanzada con OpenAI (Opcional)
```bash
pip install openai
export OPENAI_API_KEY='sk-tu-api-key'
```

### IA Avanzada con Anthropic Claude (Opcional)
```bash
pip install anthropic
export ANTHROPIC_API_KEY='sk-ant-tu-api-key'
```

---

## 📡 Endpoints de la API

### Enviar Correo con Inventario
```http
POST /api/inventarios/enviar-correo/
Authorization: Bearer <token>
Content-Type: application/json

{
    "empresa_nit": "123456789",
    "email_destino": "destino@ejemplo.com",
    "pdf_base64": "...",  // Opcional
    "incluir_analisis_ia": true,
    "incluir_blockchain": true
}
```

**Respuesta exitosa:**
```json
{
    "success": true,
    "message": "Correo enviado exitosamente a destino@ejemplo.com",
    "provider": "resend",
    "historial_id": 1,
    "hash_documento": "a1b2c3d4e5f6...",
    "alertas_count": 2,
    "details": {...}
}
```

### Obtener Análisis IA
```http
GET /api/inventarios/analisis/{empresa_nit}/
Authorization: Bearer <token>
```

**Respuesta:**
```json
{
    "success": true,
    "analisis": {
        "fecha_analisis": "2025-12-26T...",
        "metricas": {
            "total_productos": 10,
            "total_unidades": 500,
            "valor_total": 1500000,
            "pct_sin_stock": 10.0,
            "pct_stock_bajo": 20.0,
            "pct_stock_saludable": 70.0
        },
        "alertas": [...],
        "resumen": "...",
        "recomendaciones": [...]
    }
}
```

### Historial de Envíos
```http
GET /api/historial-envios/
GET /api/historial-envios/?empresa={nit}
Authorization: Bearer <token>
```

---

## 🎨 Interfaz de Usuario

El modal de envío de correo incluye:

1. **Campo de correo destino** - Validación automática
2. **Opciones avanzadas:**
   - 🤖 Análisis Inteligente (IA) - Toggle on/off
   - ⛓️ Certificación Blockchain - Toggle on/off
3. **Preview de características activas**
4. **Botón de envío con estado de carga**

---

## 📋 Prueba del Sistema

1. **Iniciar el servidor Django:**
   ```bash
   cd backend
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver 8001
   ```

2. **Iniciar el frontend:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Probar el envío:**
   - Navegar a http://localhost:5173/inventario
   - Hacer clic en "Enviar" en cualquier empresa
   - Ingresar un correo válido
   - Activar/desactivar opciones IA y Blockchain
   - Clic en "Enviar Reporte"

---

## 🔒 Seguridad

- Los tokens JWT protegen todos los endpoints de envío
- Los hashes SHA-256 garantizan la integridad del documento
- Las API keys deben configurarse como variables de entorno
- El historial de envíos registra quién envió cada correo

---

## 🐛 Troubleshooting

### Error: "RESEND_API_KEY no configurada"
- Verificar que la variable de entorno esté configurada
- Reiniciar el servidor Django después de configurar

### Error: "No se pudo enviar el correo"
- Verificar que la API key sea válida
- Revisar los logs del servidor para más detalles
- Verificar conectividad a internet

### El QR no se genera
- Instalar la librería: `pip install qrcode[pil]`
- Reiniciar el servidor

---

## 📚 Referencias

- [Resend Documentation](https://resend.com/docs)
- [Django Email](https://docs.djangoproject.com/en/5.0/topics/email/)
- [ReportLab PDF](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [QRCode Python](https://pypi.org/project/qrcode/)
