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

# Crear superusuario solo si se entregan credenciales por entorno
python manage.py shell << EOF
import os
from django.contrib.auth import get_user_model
User = get_user_model()
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
if email and password and not User.objects.filter(email=email).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print('Superuser created from environment variables.')
elif email:
    print('Superuser already exists.')
else:
    print('Superuser creation skipped. Set DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD if needed.')
EOF

if [ "$SEED_DEMO_DATA" = "true" ]; then
    echo "=== Seeding portfolio demo data ==="
    python manage.py seed_demo
fi
