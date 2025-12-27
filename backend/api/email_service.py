"""
Servicio de generación de PDF y envío de correos
Utiliza ReportLab para generar PDFs del lado del servidor
y una API REST (Resend/SendGrid) para enviar correos
"""
import base64
import io
import json
import os
from datetime import datetime

import requests
from django.conf import settings
from django.core.mail import EmailMessage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


# Colores del tema
COLORS = {
    'primary': colors.HexColor('#6366F1'),
    'secondary': colors.HexColor('#8B5CF6'),
    'success': colors.HexColor('#22C55E'),
    'warning': colors.HexColor('#F59E0B'),
    'danger': colors.HexColor('#EF4444'),
    'dark': colors.HexColor('#0F172A'),
    'gray': colors.HexColor('#64748B'),
    'light_gray': colors.HexColor('#F1F5F9'),
    'white': colors.white,
}


def generar_pdf_inventario(empresa, inventarios):
    """
    Genera un PDF del inventario de una empresa
    
    Args:
        empresa: dict con datos de la empresa (nit, nombre, direccion, telefono)
        inventarios: lista de dicts con datos del inventario
    
    Returns:
        bytes: Contenido del PDF
    """
    buffer = io.BytesIO()
    
    # Crear el documento
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=15*mm,
        leftMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm
    )
    
    # Estilos
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=COLORS['dark'],
        spaceAfter=5*mm,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=COLORS['gray'],
        spaceAfter=10*mm,
    )
    
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=COLORS['dark'],
        spaceBefore=8*mm,
        spaceAfter=5*mm,
        fontName='Helvetica-Bold'
    )
    
    # Elementos del documento
    elements = []
    
    # Título
    elements.append(Paragraph(f"📦 REPORTE DE INVENTARIO", title_style))
    elements.append(Paragraph(f"<b>{empresa.get('nombre', 'N/A')}</b>", subtitle_style))
    
    # Fecha de generación
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    elements.append(Paragraph(f"Generado: {fecha}", subtitle_style))
    elements.append(Spacer(1, 5*mm))
    
    # Información de la empresa
    elements.append(Paragraph("📋 INFORMACIÓN DE LA EMPRESA", section_style))
    
    empresa_data = [
        ['NIT:', empresa.get('nit', 'N/A'), 'Teléfono:', empresa.get('telefono', 'N/A')],
        ['Dirección:', empresa.get('direccion', 'N/A'), '', ''],
    ]
    
    empresa_table = Table(empresa_data, colWidths=[25*mm, 55*mm, 25*mm, 55*mm])
    empresa_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (0, -1), COLORS['dark']),
        ('TEXTCOLOR', (2, 0), (2, -1), COLORS['dark']),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))
    elements.append(empresa_table)
    elements.append(Spacer(1, 8*mm))
    
    # Estadísticas
    total_productos = len(inventarios)
    total_unidades = sum(inv.get('cantidad', 0) for inv in inventarios)
    stock_alto = len([inv for inv in inventarios if inv.get('cantidad', 0) > 10])
    stock_bajo = len([inv for inv in inventarios if 0 < inv.get('cantidad', 0) <= 10])
    sin_stock = len([inv for inv in inventarios if inv.get('cantidad', 0) == 0])
    
    elements.append(Paragraph("📊 RESUMEN DEL INVENTARIO", section_style))
    
    stats_data = [
        ['Total Productos', 'Total Unidades', 'Stock Alto (>10)', 'Stock Bajo (≤10)', 'Sin Stock'],
        [str(total_productos), str(total_unidades), str(stock_alto), str(stock_bajo), str(sin_stock)],
    ]
    
    stats_table = Table(stats_data, colWidths=[32*mm]*5)
    stats_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, 1), 12),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TEXTCOLOR', (0, 0), (-1, 0), COLORS['white']),
        ('TEXTCOLOR', (0, 1), (-1, 1), COLORS['dark']),
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['dark']),
        ('BACKGROUND', (0, 1), (-1, 1), COLORS['light_gray']),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, COLORS['gray']),
        ('ROUNDEDCORNERS', [3, 3, 3, 3]),
    ]))
    elements.append(stats_table)
    elements.append(Spacer(1, 8*mm))
    
    # Tabla de inventario
    if inventarios:
        elements.append(Paragraph("📦 DETALLE DEL INVENTARIO", section_style))
        
        # Header de la tabla
        table_data = [['#', 'Código', 'Producto', 'Cantidad', 'Estado', 'Actualización']]
        
        for idx, inv in enumerate(inventarios, 1):
            cantidad = inv.get('cantidad', 0)
            if cantidad == 0:
                estado = 'Sin Stock'
            elif cantidad <= 10:
                estado = 'Stock Bajo'
            else:
                estado = 'Disponible'
            
            fecha_act = inv.get('fecha_actualizacion', '')
            if fecha_act:
                try:
                    fecha_act = datetime.fromisoformat(fecha_act.replace('Z', '+00:00')).strftime('%d/%m/%Y')
                except:
                    pass
            
            table_data.append([
                str(idx),
                inv.get('producto_codigo', '-'),
                inv.get('producto_nombre', '-'),
                str(cantidad),
                estado,
                fecha_act or '-'
            ])
        
        # Fila de totales
        table_data.append(['', '', 'TOTAL', str(total_unidades), '', ''])
        
        inv_table = Table(table_data, colWidths=[10*mm, 25*mm, 55*mm, 20*mm, 25*mm, 25*mm])
        
        # Estilos base
        table_styles = [
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (2, 0), (2, -1), 'LEFT'),
            ('TEXTCOLOR', (0, 0), (-1, 0), COLORS['white']),
            ('BACKGROUND', (0, 0), (-1, 0), COLORS['dark']),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E5E5')),
            # Fila de totales
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, -1), (-1, -1), COLORS['light_gray']),
        ]
        
        # Colorear filas alternas
        for i in range(1, len(table_data) - 1):
            if i % 2 == 0:
                table_styles.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#F8FAFC')))
        
        # Colorear estados
        for i, row in enumerate(table_data[1:-1], 1):
            estado = row[4]
            if estado == 'Sin Stock':
                table_styles.append(('TEXTCOLOR', (4, i), (4, i), COLORS['danger']))
                table_styles.append(('FONTNAME', (4, i), (4, i), 'Helvetica-Bold'))
            elif estado == 'Stock Bajo':
                table_styles.append(('TEXTCOLOR', (4, i), (4, i), COLORS['warning']))
                table_styles.append(('FONTNAME', (4, i), (4, i), 'Helvetica-Bold'))
            elif estado == 'Disponible':
                table_styles.append(('TEXTCOLOR', (4, i), (4, i), COLORS['success']))
        
        inv_table.setStyle(TableStyle(table_styles))
        elements.append(inv_table)
    else:
        elements.append(Paragraph("No hay productos registrados en el inventario.", subtitle_style))
    
    # Footer
    elements.append(Spacer(1, 15*mm))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=COLORS['gray'],
        alignment=1,  # Center
    )
    elements.append(Paragraph("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", footer_style))
    elements.append(Paragraph(f"Sistema de Inventario - Lite Thinking 2025", footer_style))
    elements.append(Paragraph("Documento generado automáticamente", footer_style))
    
    # Generar PDF
    doc.build(elements)
    
    pdf_content = buffer.getvalue()
    buffer.close()
    
    return pdf_content


def enviar_correo_resend(destinatario, asunto, cuerpo_html, adjunto_pdf=None, nombre_archivo='inventario.pdf'):
    """
    Envía un correo usando la API REST de Resend
    
    Args:
        destinatario: email del destinatario
        asunto: asunto del correo
        cuerpo_html: contenido HTML del correo
        adjunto_pdf: bytes del PDF a adjuntar (opcional)
        nombre_archivo: nombre del archivo adjunto
    
    Returns:
        dict: Respuesta de la API
    """
    api_key = getattr(settings, 'RESEND_API_KEY', os.environ.get('RESEND_API_KEY', ''))
    
    if not api_key:
        raise ValueError("RESEND_API_KEY no configurada. Configura la variable de entorno o settings.RESEND_API_KEY")
    
    url = "https://api.resend.com/emails"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "from": getattr(settings, 'EMAIL_FROM', 'Inventario <onboarding@resend.dev>'),
        "to": [destinatario],
        "subject": asunto,
        "html": cuerpo_html,
    }
    
    # Agregar adjunto si existe
    if adjunto_pdf:
        payload["attachments"] = [
            {
                "filename": nombre_archivo,
                "content": base64.b64encode(adjunto_pdf).decode('utf-8'),
            }
        ]
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code not in [200, 201]:
        raise Exception(f"Error enviando correo: {response.status_code} - {response.text}")
    
    return response.json()


def enviar_correo_django(destinatario, asunto, cuerpo, adjunto_pdf=None, nombre_archivo='inventario.pdf'):
    """
    Envía un correo usando el sistema de email de Django (configuración SMTP)
    
    Args:
        destinatario: email del destinatario
        asunto: asunto del correo
        cuerpo: contenido del correo
        adjunto_pdf: bytes del PDF a adjuntar (opcional)
        nombre_archivo: nombre del archivo adjunto
    
    Returns:
        int: Número de correos enviados
    """
    email = EmailMessage(
        subject=asunto,
        body=cuerpo,
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@inventario.com'),
        to=[destinatario],
    )
    
    email.content_subtype = 'html'
    
    if adjunto_pdf:
        email.attach(nombre_archivo, adjunto_pdf, 'application/pdf')
    
    return email.send()


def generar_html_correo(empresa, total_productos, total_unidades):
    """
    Genera el cuerpo HTML del correo
    """
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
                color: white;
                padding: 30px;
                border-radius: 12px 12px 0 0;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
            }}
            .content {{
                background: #f8fafc;
                padding: 30px;
                border: 1px solid #e2e8f0;
            }}
            .stats {{
                display: flex;
                gap: 15px;
                margin: 20px 0;
            }}
            .stat-card {{
                flex: 1;
                background: white;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                border: 1px solid #e2e8f0;
            }}
            .stat-value {{
                font-size: 28px;
                font-weight: bold;
                color: #6366F1;
            }}
            .stat-label {{
                font-size: 12px;
                color: #64748b;
                text-transform: uppercase;
            }}
            .footer {{
                background: #0f172a;
                color: #94a3b8;
                padding: 20px;
                border-radius: 0 0 12px 12px;
                text-align: center;
                font-size: 12px;
            }}
            .button {{
                display: inline-block;
                background: #6366F1;
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                text-decoration: none;
                margin-top: 15px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📦 Reporte de Inventario</h1>
            <p>{empresa.get('nombre', 'N/A')}</p>
        </div>
        <div class="content">
            <p>Hola,</p>
            <p>Adjunto encontrarás el reporte de inventario de <strong>{empresa.get('nombre', 'N/A')}</strong> generado el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}.</p>
            
            <table style="width: 100%; border-collapse: separate; border-spacing: 10px;">
                <tr>
                    <td style="background: white; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0;">
                        <div style="font-size: 28px; font-weight: bold; color: #6366F1;">{total_productos}</div>
                        <div style="font-size: 12px; color: #64748b; text-transform: uppercase;">Productos</div>
                    </td>
                    <td style="background: white; padding: 15px; border-radius: 8px; text-align: center; border: 1px solid #e2e8f0;">
                        <div style="font-size: 28px; font-weight: bold; color: #8B5CF6;">{total_unidades}</div>
                        <div style="font-size: 12px; color: #64748b; text-transform: uppercase;">Unidades</div>
                    </td>
                </tr>
            </table>
            
            <p style="margin-top: 20px; padding: 15px; background: #fef3c7; border-radius: 8px; border-left: 4px solid #f59e0b;">
                📎 El reporte completo en formato PDF se encuentra adjunto a este correo.
            </p>
        </div>
        <div class="footer">
            <p>Sistema de Inventario - Lite Thinking 2025</p>
            <p>Este es un correo automático, por favor no responder.</p>
        </div>
    </body>
    </html>
    """
