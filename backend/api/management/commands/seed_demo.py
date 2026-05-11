import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from litethinking_domain.models import Empresa, Inventario, Producto


DEMO_EMPRESAS = [
    {
        'nit': '900100200-1',
        'nombre': 'Andes Retail Group',
        'direccion': 'Cra 11 # 82-71, Bogota',
        'telefono': '+57 601 555 0101',
    },
    {
        'nit': '901555777-4',
        'nombre': 'Clinica Norte Supply',
        'direccion': 'Av. 19 # 120-45, Bogota',
        'telefono': '+57 601 555 0202',
    },
    {
        'nit': '830222333-8',
        'nombre': 'Cafe Sierra Export',
        'direccion': 'Calle 10 # 5-44, Manizales',
        'telefono': '+57 606 555 0303',
    },
]

DEMO_PRODUCTOS = [
    {
        'empresa_nit': '900100200-1',
        'codigo': 'RET-POS-001',
        'nombre': 'Terminal POS Pro',
        'caracteristicas': 'Equipo de punto de venta para tiendas de alto trafico.',
        'precios': {'COP': 1850000, 'USD': 470},
        'cantidad': 12,
    },
    {
        'empresa_nit': '900100200-1',
        'codigo': 'RET-SCAN-014',
        'nombre': 'Scanner industrial Zebra',
        'caracteristicas': 'Lector de codigo de barras resistente para bodega.',
        'precios': {'COP': 980000, 'USD': 250},
        'cantidad': 4,
    },
    {
        'empresa_nit': '900100200-1',
        'codigo': 'RET-TAG-220',
        'nombre': 'Etiquetas RFID premium',
        'caracteristicas': 'Paquete de etiquetas para trazabilidad de inventario.',
        'precios': {'COP': 220000, 'USD': 56},
        'cantidad': 0,
    },
    {
        'empresa_nit': '901555777-4',
        'codigo': 'MED-GLOVE-100',
        'nombre': 'Guantes nitrilo caja x100',
        'caracteristicas': 'Insumo medico de alta rotacion.',
        'precios': {'COP': 42000, 'USD': 11},
        'cantidad': 86,
    },
    {
        'empresa_nit': '901555777-4',
        'codigo': 'MED-MASK-050',
        'nombre': 'Mascarilla quirurgica x50',
        'caracteristicas': 'Caja de mascarillas para area clinica.',
        'precios': {'COP': 28000, 'USD': 7},
        'cantidad': 7,
    },
    {
        'empresa_nit': '901555777-4',
        'codigo': 'MED-SERUM-500',
        'nombre': 'Suero fisiologico 500ml',
        'caracteristicas': 'Unidad esteril para procedimientos generales.',
        'precios': {'COP': 11500, 'USD': 3},
        'cantidad': 0,
    },
    {
        'empresa_nit': '830222333-8',
        'codigo': 'CAF-GRN-001',
        'nombre': 'Cafe verde pergamino 70kg',
        'caracteristicas': 'Saco de cafe verde tipo exportacion.',
        'precios': {'COP': 1080000, 'USD': 275},
        'cantidad': 32,
    },
    {
        'empresa_nit': '830222333-8',
        'codigo': 'CAF-BAG-250',
        'nombre': 'Bolsa valvula 250g',
        'caracteristicas': 'Empaque metalizado con valvula desgasificadora.',
        'precios': {'COP': 950, 'USD': 0.24},
        'cantidad': 480,
    },
    {
        'empresa_nit': '830222333-8',
        'codigo': 'CAF-LAB-010',
        'nombre': 'Kit catacion laboratorio',
        'caracteristicas': 'Set para control de calidad de lotes especiales.',
        'precios': {'COP': 640000, 'USD': 162},
        'cantidad': 6,
    },
]


class Command(BaseCommand):
    help = 'Create portfolio demo users, companies, products, and inventory.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing seeded demo companies and products before recreating them.',
        )
        parser.add_argument(
            '--skip-users',
            action='store_true',
            help='Only seed business data; do not create demo users.',
        )

    def handle(self, *args, **options):
        if options['reset']:
            demo_nits = [empresa['nit'] for empresa in DEMO_EMPRESAS]
            Producto.objects.filter(empresa__nit__in=demo_nits).delete()
            Empresa.objects.filter(nit__in=demo_nits).delete()
            self.stdout.write(self.style.WARNING('Existing demo business data removed.'))

        empresas = {}
        for empresa_data in DEMO_EMPRESAS:
            empresa, _ = Empresa.objects.update_or_create(
                nit=empresa_data['nit'],
                defaults={
                    'nombre': empresa_data['nombre'],
                    'direccion': empresa_data['direccion'],
                    'telefono': empresa_data['telefono'],
                },
            )
            empresas[empresa.nit] = empresa

        for producto_data in DEMO_PRODUCTOS:
            producto, _ = Producto.objects.update_or_create(
                codigo=producto_data['codigo'],
                defaults={
                    'nombre': producto_data['nombre'],
                    'caracteristicas': producto_data['caracteristicas'],
                    'precios': producto_data['precios'],
                    'empresa': empresas[producto_data['empresa_nit']],
                },
            )
            Inventario.objects.update_or_create(
                producto=producto,
                defaults={'cantidad': producto_data['cantidad']},
            )

        if not options['skip_users']:
            self._seed_users()

        self.stdout.write(self.style.SUCCESS(
            f"Demo ready: {len(DEMO_EMPRESAS)} companies, "
            f"{len(DEMO_PRODUCTOS)} products, and demo users."
        ))

    def _seed_users(self):
        User = get_user_model()
        admin_email = os.environ.get('DEMO_ADMIN_EMAIL', 'admin.demo@example.com')
        admin_password = os.environ.get('DEMO_ADMIN_PASSWORD', 'DemoAdmin2026!')
        viewer_email = os.environ.get('DEMO_USER_EMAIL', 'demo@example.com')
        viewer_password = os.environ.get('DEMO_USER_PASSWORD', 'DemoUser2026!')

        admin_user, _ = User.objects.update_or_create(
            email=admin_email,
            defaults={
                'username': os.environ.get('DEMO_ADMIN_USERNAME', 'admin_demo'),
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
            },
        )
        admin_user.set_password(admin_password)
        admin_user.save()

        viewer_user, _ = User.objects.update_or_create(
            email=viewer_email,
            defaults={
                'username': os.environ.get('DEMO_USER_USERNAME', 'demo_viewer'),
                'is_staff': False,
                'is_superuser': False,
                'is_active': True,
            },
        )
        viewer_user.set_password(viewer_password)
        viewer_user.save()
