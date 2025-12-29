#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias del proyecto
pip install -r requirements.txt

# Instalar el paquete de dominio desde el directorio local
# En producción, esto podría ser desde PyPI: pip install litethinking-domain
if [ -d "../domain" ]; then
    echo "Instalando paquete de dominio local..."
    pip install -e ../domain
else
    echo "Advertencia: Directorio domain no encontrado. Usando solo dependencias base."
fi

python manage.py collectstatic --no-input
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
