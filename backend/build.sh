#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias del proyecto
pip install --upgrade pip
pip install -r requirements.txt

# Instalar el paquete de dominio
# El directorio domain está en el mismo repo, un nivel arriba
DOMAIN_PATH="../domain"
if [ -d "$DOMAIN_PATH" ]; then
    echo "=== Instalando paquete de dominio desde: $DOMAIN_PATH ==="
    pip install "$DOMAIN_PATH"
    echo "=== Paquete de dominio instalado exitosamente ==="
else
    echo "ERROR: No se encontró el directorio domain en: $DOMAIN_PATH"
    echo "La estructura debe ser:"
    echo "  repo/"
    echo "    ├── backend/"
    echo "    └── domain/"
    exit 1
fi

python manage.py collectstatic --no-input

# Primero marcar como fake la migración inicial de litethinking_domain
# porque las tablas core_* ya existen en producción
echo "=== Aplicando migraciones ==="
python manage.py migrate litethinking_domain --fake-initial
python manage.py migrate

# Crear superusuario si no existe
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admins@gmail.com').exists():
    User.objects.create_superuser(
        username='admin',
        email='admins@gmail.com',
        password='12345678'
    )
    print('Superuser created!')
else:
    print('Superuser already exists.')
EOF
