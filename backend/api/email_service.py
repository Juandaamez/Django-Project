"""
Servicio de generación de PDF y envío de correos
Utiliza ReportLab para generar PDFs del lado del servidor
y una API REST (Resend/SendGrid) para enviar correos

Diseño: Moderno, Minimalista y Profesional
"""
import base64
import io
import json
import os
from datetime import datetime
import locale

import requests
from django.conf import settings
from django.core.mail import EmailMessage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm, inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
    Image,
    HRFlowable,
    KeepTogether,
    PageBreak,
)
from reportlab.graphics.shapes import Drawing, Rect, String, Circle, Line
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF


# Paleta de colores moderna y elegante
COLORS = {
    # Colores principales
    'primary': colors.HexColor('#0F172A'),      # Slate 900 - Header oscuro
    'primary_light': colors.HexColor('#1E293B'), # Slate 800
    'accent': colors.HexColor('#6366F1'),        # Indigo 500 - Acentos
    'accent_light': colors.HexColor('#818CF8'),  # Indigo 400
    
    # Estados
    'success': colors.HexColor('#10B981'),       # Emerald 500
    'success_light': colors.HexColor('#D1FAE5'), # Emerald 100
    'warning': colors.HexColor('#F59E0B'),       # Amber 500
    'warning_light': colors.HexColor('#FEF3C7'), # Amber 100
    'danger': colors.HexColor('#EF4444'),        # Red 500
    'danger_light': colors.HexColor('#FEE2E2'),  # Red 100
    
    # Neutros
    'text_primary': colors.HexColor('#0F172A'),  # Slate 900
    'text_secondary': colors.HexColor('#475569'), # Slate 600
    'text_muted': colors.HexColor('#94A3B8'),    # Slate 400
    'border': colors.HexColor('#E2E8F0'),        # Slate 200
    'bg_light': colors.HexColor('#F8FAFC'),      # Slate 50
    'bg_card': colors.HexColor('#FFFFFF'),       # White
    'white': colors.white,
}


def _format_currency(value, currency='COP'):
    """Formatea valores monetarios"""
    try:
        if currency == 'COP':
            return f"${value:,.0f}".replace(',', '.')
        return f"${value:,.2f}"
    except:
        return str(value)


def _format_date(date_str):
    """Formatea fechas de manera elegante"""
    if not date_str:
        return '-'
    try:
        if isinstance(date_str, str):
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        else:
            dt = date_str
        return dt.strftime('%d %b %Y')
    except:
        return str(date_str)


def _get_status_color(cantidad):
    """Retorna colores según el estado del stock"""
    if cantidad == 0:
        return COLORS['danger'], COLORS['danger_light'], 'SIN STOCK'
    elif cantidad <= 10:
        return COLORS['warning'], COLORS['warning_light'], 'STOCK BAJO'
    else:
        return COLORS['success'], COLORS['success_light'], 'DISPONIBLE'


def _draw_header(canvas_obj, doc, empresa, fecha_generacion):
    """Dibuja el header elegante del documento"""
    width, height = A4
    
    # Fondo del header - gradiente simulado con rectángulos
    canvas_obj.setFillColor(COLORS['primary'])
    canvas_obj.rect(0, height - 85*mm, width, 85*mm, fill=1, stroke=0)
    
    # Línea de acento superior
    canvas_obj.setFillColor(COLORS['accent'])
    canvas_obj.rect(0, height - 3*mm, width, 3*mm, fill=1, stroke=0)
    
    # Logo / Marca (simulado con texto estilizado)
    canvas_obj.setFillColor(COLORS['white'])
    canvas_obj.setFont('Helvetica-Bold', 10)
    canvas_obj.drawString(25*mm, height - 18*mm, 'LITE THINKING')
    
    canvas_obj.setFillColor(COLORS['accent_light'])
    canvas_obj.setFont('Helvetica', 8)
    canvas_obj.drawString(25*mm, height - 23*mm, 'Sistema de Inventario')
    
    # Título principal centrado
    canvas_obj.setFillColor(COLORS['white'])
    canvas_obj.setFont('Helvetica-Bold', 24)
    canvas_obj.drawCentredString(width/2, height - 45*mm, 'REPORTE DE INVENTARIO')
    
    # Nombre de empresa
    canvas_obj.setFillColor(COLORS['accent_light'])
    canvas_obj.setFont('Helvetica', 14)
    canvas_obj.drawCentredString(width/2, height - 55*mm, empresa.get('nombre', 'N/A').upper())
    
    # Fecha de generación (esquina derecha)
    canvas_obj.setFillColor(COLORS['text_muted'])
    canvas_obj.setFont('Helvetica', 8)
    canvas_obj.drawRightString(width - 25*mm, height - 18*mm, f'Generado: {fecha_generacion}')
    
    # Línea decorativa inferior del header
    canvas_obj.setStrokeColor(COLORS['accent'])
    canvas_obj.setLineWidth(2)
    canvas_obj.line(25*mm, height - 70*mm, width - 25*mm, height - 70*mm)


def _draw_footer(canvas_obj, doc):
    """Dibuja el footer del documento"""
    width, height = A4
    
    # Línea superior del footer
    canvas_obj.setStrokeColor(COLORS['border'])
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(25*mm, 20*mm, width - 25*mm, 20*mm)
    
    # Texto del footer
    canvas_obj.setFillColor(COLORS['text_muted'])
    canvas_obj.setFont('Helvetica', 7)
    canvas_obj.drawString(25*mm, 14*mm, 'Sistema de Inventario - Lite Thinking © 2025')
    canvas_obj.drawCentredString(width/2, 14*mm, f'Página {doc.page}')
    canvas_obj.drawRightString(width - 25*mm, 14*mm, 'Documento confidencial')


def _create_stat_card(label, value, color=None, width_card=42*mm):
    """Crea una tarjeta de estadística como tabla"""
    if color is None:
        color = COLORS['accent']
    
    data = [
        [value],
        [label]
    ]
    
    table = Table(data, colWidths=[width_card])
    table.setStyle(TableStyle([
        # Valor
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (0, 0), 22),
        ('TEXTCOLOR', (0, 0), (0, 0), color),
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (0, 0), 2),
        ('TOPPADDING', (0, 0), (0, 0), 12),
        # Label
        ('FONTNAME', (0, 1), (0, 1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (0, 1), 8),
        ('TEXTCOLOR', (0, 1), (0, 1), COLORS['text_secondary']),
        ('ALIGN', (0, 1), (0, 1), 'CENTER'),
        ('BOTTOMPADDING', (0, 1), (0, 1), 12),
        # General
        ('BACKGROUND', (0, 0), (0, -1), COLORS['bg_light']),
        ('BOX', (0, 0), (-1, -1), 0.5, COLORS['border']),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return table


def generar_pdf_inventario(empresa, inventarios):
    """
    Genera un PDF profesional y minimalista del inventario
    
    Args:
        empresa: dict con datos de la empresa (nit, nombre, direccion, telefono)
        inventarios: lista de dicts con datos del inventario
    
    Returns:
        bytes: Contenido del PDF
    """
    buffer = io.BytesIO()
    width, height = A4
    
    # Fecha de generación formateada
    fecha_generacion = datetime.now().strftime('%d de %B, %Y').capitalize()
    
    # Crear el documento con márgenes personalizados
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=25*mm,
        leftMargin=25*mm,
        topMargin=95*mm,  # Espacio para el header
        bottomMargin=30*mm  # Espacio para el footer
    )
    
    # Estilos personalizados
    styles = getSampleStyleSheet()
    
    # Estilo para secciones
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Helvetica-Bold',
        textColor=COLORS['text_primary'],
        spaceBefore=8*mm,
        spaceAfter=4*mm,
        leftIndent=0,
    )
    
    # Estilo para texto normal
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Helvetica',
        textColor=COLORS['text_secondary'],
        leading=14,
    )
    
    # Estilo para labels
    label_style = ParagraphStyle(
        'Label',
        parent=styles['Normal'],
        fontSize=8,
        fontName='Helvetica',
        textColor=COLORS['text_muted'],
    )
    
    # Estilo para valores
    value_style = ParagraphStyle(
        'Value',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica-Bold',
        textColor=COLORS['text_primary'],
    )
    
    elements = []
    
    # ═══════════════════════════════════════════════════════════════
    # SECCIÓN: INFORMACIÓN DE LA EMPRESA
    # ═══════════════════════════════════════════════════════════════
    
    elements.append(Paragraph('INFORMACIÓN DE LA EMPRESA', section_title_style))
    
    # Tarjeta de información de empresa
    empresa_info = [
        [
            Paragraph('<font size="7" color="#94A3B8">NIT</font>', label_style),
            Paragraph('<font size="7" color="#94A3B8">TELÉFONO</font>', label_style),
        ],
        [
            Paragraph(f'<font size="10"><b>{empresa.get("nit", "N/A")}</b></font>', value_style),
            Paragraph(f'<font size="10"><b>{empresa.get("telefono", "N/A")}</b></font>', value_style),
        ],
        [
            Paragraph('<font size="7" color="#94A3B8">DIRECCIÓN</font>', label_style),
            Paragraph('', label_style),
        ],
        [
            Paragraph(f'<font size="10"><b>{empresa.get("direccion", "N/A")}</b></font>', value_style),
            Paragraph('', value_style),
        ],
    ]
    
    empresa_table = Table(empresa_info, colWidths=[80*mm, 80*mm])
    empresa_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('BACKGROUND', (0, 0), (-1, -1), COLORS['bg_light']),
        ('BOX', (0, 0), (-1, -1), 0.5, COLORS['border']),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(empresa_table)
    elements.append(Spacer(1, 8*mm))
    
    # ═══════════════════════════════════════════════════════════════
    # SECCIÓN: RESUMEN ESTADÍSTICO
    # ═══════════════════════════════════════════════════════════════
    
    elements.append(Paragraph('RESUMEN DEL INVENTARIO', section_title_style))
    
    # Calcular estadísticas
    total_productos = len(inventarios)
    total_unidades = sum(inv.get('cantidad', 0) for inv in inventarios)
    stock_alto = len([inv for inv in inventarios if inv.get('cantidad', 0) > 10])
    stock_bajo = len([inv for inv in inventarios if 0 < inv.get('cantidad', 0) <= 10])
    sin_stock = len([inv for inv in inventarios if inv.get('cantidad', 0) == 0])
    
    # Calcular valor total del inventario si hay precios
    valor_total = sum(
        inv.get('cantidad', 0) * inv.get('producto_precio', 0) 
        for inv in inventarios
    )
    
    # Tarjetas de estadísticas en fila
    stats_row = [
        [
            _create_stat_card('Productos', str(total_productos), COLORS['accent']),
            _create_stat_card('Unidades', str(total_unidades), COLORS['primary']),
            _create_stat_card('Stock Alto', str(stock_alto), COLORS['success']),
            _create_stat_card('Stock Bajo', str(stock_bajo), COLORS['warning']),
        ]
    ]
    
    stats_table = Table(stats_row, colWidths=[42*mm]*4)
    stats_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 2),
    ]))
    elements.append(stats_table)
    
    # Barra de estado del inventario (visual)
    elements.append(Spacer(1, 5*mm))
    
    if total_productos > 0:
        # Calcular porcentajes
        pct_alto = (stock_alto / total_productos) * 100 if total_productos > 0 else 0
        pct_bajo = (stock_bajo / total_productos) * 100 if total_productos > 0 else 0
        pct_sin = (sin_stock / total_productos) * 100 if total_productos > 0 else 0
        
        # Crear barra visual de distribución
        distribution_data = [[
            Paragraph(f'<font size="7" color="#FFFFFF"><b>{pct_alto:.0f}%</b></font>', 
                     ParagraphStyle('', alignment=TA_CENTER)) if pct_alto > 5 else '',
            Paragraph(f'<font size="7" color="#FFFFFF"><b>{pct_bajo:.0f}%</b></font>', 
                     ParagraphStyle('', alignment=TA_CENTER)) if pct_bajo > 5 else '',
            Paragraph(f'<font size="7" color="#FFFFFF"><b>{pct_sin:.0f}%</b></font>', 
                     ParagraphStyle('', alignment=TA_CENTER)) if pct_sin > 5 else '',
        ]]
        
        # Anchos proporcionales (mínimo 5mm para visibilidad)
        total_width = 160*mm
        w_alto = max(5*mm, (pct_alto / 100) * total_width) if pct_alto > 0 else 0
        w_bajo = max(5*mm, (pct_bajo / 100) * total_width) if pct_bajo > 0 else 0
        w_sin = max(5*mm, (pct_sin / 100) * total_width) if pct_sin > 0 else 0
        
        if w_alto + w_bajo + w_sin > 0:
            dist_table = Table(distribution_data, colWidths=[w_alto, w_bajo, w_sin])
            dist_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, 0), COLORS['success']),
                ('BACKGROUND', (1, 0), (1, 0), COLORS['warning']),
                ('BACKGROUND', (2, 0), (2, 0), COLORS['danger']),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            elements.append(dist_table)
        
        # Leyenda de la barra
        legend_data = [[
            Paragraph('<font size="7">● Stock Alto</font>', 
                     ParagraphStyle('', textColor=COLORS['success'])),
            Paragraph('<font size="7">● Stock Bajo</font>', 
                     ParagraphStyle('', textColor=COLORS['warning'])),
            Paragraph('<font size="7">● Sin Stock</font>', 
                     ParagraphStyle('', textColor=COLORS['danger'])),
        ]]
        legend_table = Table(legend_data, colWidths=[53*mm]*3)
        legend_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
        ]))
        elements.append(legend_table)
    
    elements.append(Spacer(1, 8*mm))
    
    # ═══════════════════════════════════════════════════════════════
    # SECCIÓN: DETALLE DEL INVENTARIO
    # ═══════════════════════════════════════════════════════════════
    
    elements.append(Paragraph('DETALLE DEL INVENTARIO', section_title_style))
    
    if inventarios:
        # Header de la tabla con diseño moderno
        header_style = ParagraphStyle(
            'TableHeader',
            fontSize=7,
            fontName='Helvetica-Bold',
            textColor=COLORS['white'],
            alignment=TA_CENTER,
        )
        
        cell_style = ParagraphStyle(
            'TableCell',
            fontSize=8,
            fontName='Helvetica',
            textColor=COLORS['text_primary'],
        )
        
        cell_center_style = ParagraphStyle(
            'TableCellCenter',
            fontSize=8,
            fontName='Helvetica',
            textColor=COLORS['text_primary'],
            alignment=TA_CENTER,
        )
        
        # Construir datos de la tabla
        table_data = [[
            Paragraph('#', header_style),
            Paragraph('CÓDIGO', header_style),
            Paragraph('PRODUCTO', header_style),
            Paragraph('CANTIDAD', header_style),
            Paragraph('ESTADO', header_style),
            Paragraph('PRECIO', header_style),
        ]]
        
        for idx, inv in enumerate(inventarios, 1):
            cantidad = inv.get('cantidad', 0)
            status_color, status_bg, status_text = _get_status_color(cantidad)
            precio = inv.get('producto_precio', 0)
            
            # Crear badge de estado
            status_para = Paragraph(
                f'<font size="7" color="{status_color.hexval()}">{status_text}</font>',
                ParagraphStyle('StatusBadge', alignment=TA_CENTER)
            )
            
            table_data.append([
                Paragraph(f'<font size="8">{idx}</font>', cell_center_style),
                Paragraph(f'<font size="8" name="Courier"><b>{inv.get("producto_codigo", "-")}</b></font>', cell_style),
                Paragraph(f'<font size="8">{inv.get("producto_nombre", "-")}</font>', cell_style),
                Paragraph(f'<font size="9"><b>{cantidad}</b></font>', cell_center_style),
                status_para,
                Paragraph(f'<font size="8">{_format_currency(precio)}</font>', cell_center_style),
            ])
        
        # Fila de totales
        table_data.append([
            '',
            '',
            Paragraph('<font size="8"><b>TOTAL</b></font>', cell_style),
            Paragraph(f'<font size="9"><b>{total_unidades}</b></font>', cell_center_style),
            '',
            Paragraph(f'<font size="8"><b>{_format_currency(valor_total)}</b></font>', cell_center_style),
        ])
        
        # Crear tabla con anchos optimizados
        inv_table = Table(
            table_data, 
            colWidths=[12*mm, 28*mm, 58*mm, 22*mm, 25*mm, 25*mm],
            repeatRows=1  # Repetir header en cada página
        )
        
        # Estilos de la tabla
        table_styles = [
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), COLORS['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), COLORS['white']),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 7),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            
            # Cuerpo
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Alineaciones
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (3, 0), (3, -1), 'CENTER'),
            ('ALIGN', (4, 0), (4, -1), 'CENTER'),
            ('ALIGN', (5, 0), (5, -1), 'CENTER'),
            
            # Bordes sutiles
            ('LINEBELOW', (0, 0), (-1, 0), 1, COLORS['primary']),
            ('LINEBELOW', (0, 1), (-1, -2), 0.25, COLORS['border']),
            
            # Fila de totales
            ('BACKGROUND', (0, -1), (-1, -1), COLORS['bg_light']),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('LINEABOVE', (0, -1), (-1, -1), 1, COLORS['primary']),
        ]
        
        # Alternar colores de fila para mejor legibilidad
        for i in range(1, len(table_data) - 1):
            if i % 2 == 0:
                table_styles.append(('BACKGROUND', (0, i), (-1, i), COLORS['bg_light']))
        
        # Colorear fondo de estados
        for i, inv in enumerate(inventarios, 1):
            cantidad = inv.get('cantidad', 0)
            _, status_bg, _ = _get_status_color(cantidad)
            table_styles.append(('BACKGROUND', (4, i), (4, i), status_bg))
        
        inv_table.setStyle(TableStyle(table_styles))
        elements.append(inv_table)
        
    else:
        # Estado vacío elegante
        empty_data = [[
            Paragraph(
                '<font size="10" color="#94A3B8">No hay productos registrados en el inventario</font>',
                ParagraphStyle('Empty', alignment=TA_CENTER)
            )
        ]]
        empty_table = Table(empty_data, colWidths=[160*mm])
        empty_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), COLORS['bg_light']),
            ('BOX', (0, 0), (-1, -1), 0.5, COLORS['border']),
            ('TOPPADDING', (0, 0), (-1, -1), 25),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 25),
        ]))
        elements.append(empty_table)
    
    # ═══════════════════════════════════════════════════════════════
    # CONSTRUIR PDF
    # ═══════════════════════════════════════════════════════════════
    
    def add_header_footer(canvas_obj, doc):
        """Callback para agregar header y footer en cada página"""
        canvas_obj.saveState()
        _draw_header(canvas_obj, doc, empresa, fecha_generacion)
        _draw_footer(canvas_obj, doc)
        canvas_obj.restoreState()
    
    # Generar el documento
    doc.build(elements, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    
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
