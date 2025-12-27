#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

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
