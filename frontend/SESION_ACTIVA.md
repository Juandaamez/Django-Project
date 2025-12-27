# 🎨 Sistema de Sesión Activa - Frontend

## ✨ Nuevas Funcionalidades Implementadas

Se ha implementado un sistema visual completo para mostrar el estado de sesión activa en la página principal, siguiendo la arquitectura de **Atomic Design**.

### 🧩 Componentes Creados

#### Átomos

- **`UserBadge`**: Badge circular con avatar generado a partir de las iniciales del usuario, incluye indicador de estado online animado.

#### Moléculas

- **`UserProfileDropdown`**: Menú desplegable con información del usuario, acciones rápidas y botón de cierre de sesión. Incluye indicador especial para administradores.
- **`WelcomeBanner`**: Banner flotante de bienvenida que aparece automáticamente al iniciar sesión. Se muestra una sola vez por sesión con animaciones suaves.

#### Organismos

- **`NavigationBar`**: Barra de navegación superior fija con:
  - Logo e identidad de marca
  - Enlaces de navegación (adaptativos según autenticación)
  - Indicador de "Sesión activa" con punto verde pulsante
  - Menú de perfil de usuario integrado
  - Diseño responsive con navegación móvil

### 🎯 Características Destacadas

1. **Identificación Visual del Usuario**

   - Avatar con gradiente de colores basado en el nombre
   - Indicador de estado online con animación pulsante
   - Nombre y email del usuario visible en el dropdown
2. **Contenido Dinámico**

   - El hero de la página principal cambia según el estado de autenticación
   - Mensaje personalizado con el nombre del usuario cuando está logueado
   - Botones de acción adaptativos (Login vs Dashboard)
3. **Indicadores de Estado**

   - Badge de "Sesión activa" en la navbar (escritorio)
   - Punto verde animado en el avatar
   - Banner de bienvenida al iniciar sesión (auto-oculta)
4. **Roles y Permisos**

   - Identificación visual de usuarios administradores
   - Acceso especial a "Panel Admin" para administradores
   - Links de navegación filtrados según permisos
5. **Animaciones y Transiciones**

   - Animación shimmer en el banner de bienvenida
   - Transiciones suaves en todos los elementos interactivos
   - Efectos hover con escalado y cambio de color
   - Dropdown con animación slide-in

### 📱 Diseño Responsive

- **Desktop**: Navegación completa con todos los indicadores
- **Tablet**: Menú adaptado con elementos principales
- **Mobile**: Navegación colapsable con scroll horizontal

### 🎨 Sistema de Colores

El sistema utiliza gradientes dinámicos para los avatares:

- Azul-Cyan
- Morado-Rosa
- Verde-Esmeralda
- Naranja-Ámbar
- Rojo-Rosa

Los colores se asignan basándose en el nombre del usuario para consistencia.

### 🔐 Seguridad

- Utiliza el `AuthContext` para verificar autenticación
- Session storage para controlar la visualización del banner
- Logout seguro con limpieza de estado
- Rutas protegidas integradas

### 🚀 Uso

Los componentes se integran automáticamente cuando el usuario inicia sesión. No requiere configuración adicional.

```jsx
// El LandingTemplate ya incluye todos los componentes
<LandingTemplate hero={heroContent} sections={sections} workflow={workflowContent} />
```

### 📦 Archivos Modificados/Creados

**Nuevos componentes:**

- `src/components/atoms/UserBadge.jsx`
- `src/components/molecules/UserProfileDropdown.jsx`
- `src/components/molecules/WelcomeBanner.jsx`
- `src/components/organisms/NavigationBar.jsx`

**Archivos actualizados:**

- `src/components/templates/LandingTemplate.jsx`
- `src/routes/AppRoutes.jsx`
- `src/index.css` (animación shimmer)
- Todos los archivos `index.js` de export
