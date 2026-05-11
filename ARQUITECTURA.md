# Arquitectura

Este proyecto esta organizado como una aplicacion fullstack con tres bloques
principales: frontend React, backend Django REST y un paquete local de dominio.

## Vista general

```text
frontend/  -> UI React, rutas, contexto de autenticacion y clientes Axios
backend/   -> API REST, permisos, servicios de PDF/correo/analisis y comandos
domain/    -> paquete Python instalable con modelos Django del negocio
```

## Flujo de datos

```text
React UI -> Axios services -> Django REST Framework -> modelos del paquete domain
                                      |
                                      +-> ReportLab PDF
                                      +-> Hash SHA-256
                                      +-> Resend/Django SMTP o simulacion demo
```

## Frontend

La capa de presentacion usa React, Vite y TailwindCSS. La estructura sigue
Atomic Design:

```text
src/components/atoms
src/components/molecules
src/components/organisms
src/components/templates
```

Las paginas consumen servicios especializados:

- `empresa.service.js`
- `producto.service.js`
- `inventario.service.js`
- `auth.service.js`

La sesion se gestiona con `AuthContext` y tokens JWT guardados en
`localStorage`.

## Backend

El backend expone endpoints REST con Django REST Framework:

- `/api/auth/login/`
- `/api/auth/token/refresh/`
- `/api/empresas/`
- `/api/productos/`
- `/api/inventarios/`
- `/api/inventarios/pdf/<empresa_nit>/`
- `/api/inventarios/enviar-correo/`
- `/api/inventarios/analisis/<empresa_nit>/`
- `/api/historial-envios/`

Tambien publica documentacion OpenAPI en:

- `/api/schema/`
- `/api/docs/`
- `/api/redoc/`

## Paquete de dominio

`domain/` contiene `litethinking-domain`, un paquete Python instalable. En esta
version el paquete contiene los modelos Django ORM del negocio:

- `Empresa`
- `Producto`
- `Inventario`
- `HistorialEnvio`

Esto permite que los modelos vivan fuera del proyecto Django principal y se
instalen en el backend con:

```bash
pip install -e ../domain
```

## Modo demo

El proyecto incluye un modo demo para portafolio:

```bash
python manage.py seed_demo
```

Este comando crea usuarios, empresas, productos e inventarios con casos
interesantes para mostrar alertas de stock. Si `DEMO_MODE=True` y no hay
`RESEND_API_KEY`, el endpoint de envio de correo simula el envio y guarda el
historial, de modo que la demo siga funcionando sin servicios externos.

## Decisiones tecnicas

- Los endpoints de lectura de empresas/productos pueden verse publicamente.
- Las mutaciones requieren usuario staff.
- Inventario, PDF, analisis e historial requieren autenticacion.
- El hash SHA-256 certifica el PDF y una representacion canonica del inventario.
- El deploy puede sembrar datos automaticamente con `SEED_DEMO_DATA=true`.

## Mejoras futuras

- Separar entidades puras del dominio si se quiere una Clean Architecture mas estricta.
- Agregar tests frontend con React Testing Library o Playwright.
- Agregar un endpoint publico de verificacion de hash.
- Reemplazar el analisis por reglas con un proveedor IA configurable.
