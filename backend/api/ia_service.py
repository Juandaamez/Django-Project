"""
Servicio de Análisis Inteligente de Inventario (IA)

Este módulo proporciona análisis automático del inventario usando
técnicas de análisis de datos para generar:
- Alertas de stock bajo/agotado
- Recomendaciones de reabastecimiento
- Análisis de valor del inventario
- Detección de patrones y anomalías
- Resúmenes ejecutivos inteligentes

Nota: Para IA más avanzada (GPT, Claude, etc.), configurar:
- OPENAI_API_KEY para análisis con GPT
- ANTHROPIC_API_KEY para análisis con Claude
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple
from decimal import Decimal

# Intentar importar librerías de IA opcionales
try:
    import openai
    OPENAI_DISPONIBLE = True
except ImportError:
    OPENAI_DISPONIBLE = False

try:
    import anthropic
    ANTHROPIC_DISPONIBLE = True
except ImportError:
    ANTHROPIC_DISPONIBLE = False


class AnalisisInventarioIA:
    """
    Motor de análisis inteligente para inventarios.
    Proporciona insights, alertas y recomendaciones automáticas.
    """
    
    # Umbrales configurables
    UMBRAL_STOCK_CRITICO = 0
    UMBRAL_STOCK_BAJO = 10
    UMBRAL_STOCK_MEDIO = 50
    UMBRAL_VALOR_ALTO = 1000000  # COP
    
    def __init__(self, empresa: dict, inventarios: list):
        self.empresa = empresa
        self.inventarios = inventarios
        self.fecha_analisis = datetime.now()
        
        # Calcular métricas base
        self._calcular_metricas()
    
    def _calcular_metricas(self):
        """Calcula métricas base del inventario"""
        self.total_productos = len(self.inventarios)
        self.total_unidades = sum(inv.get('cantidad', 0) for inv in self.inventarios)
        
        # Clasificar productos por stock
        self.productos_sin_stock = []
        self.productos_stock_bajo = []
        self.productos_stock_medio = []
        self.productos_stock_alto = []
        
        self.valor_total = Decimal('0')
        
        for inv in self.inventarios:
            cantidad = inv.get('cantidad', 0)
            precio = Decimal(str(inv.get('producto_precio', 0) or 0))
            valor = cantidad * precio
            self.valor_total += valor
            
            producto_info = {
                'codigo': inv.get('producto_codigo', 'N/A'),
                'nombre': inv.get('producto_nombre', 'N/A'),
                'cantidad': cantidad,
                'precio': float(precio),
                'valor': float(valor),
            }
            
            if cantidad == self.UMBRAL_STOCK_CRITICO:
                self.productos_sin_stock.append(producto_info)
            elif cantidad <= self.UMBRAL_STOCK_BAJO:
                self.productos_stock_bajo.append(producto_info)
            elif cantidad <= self.UMBRAL_STOCK_MEDIO:
                self.productos_stock_medio.append(producto_info)
            else:
                self.productos_stock_alto.append(producto_info)
        
        # Porcentajes
        if self.total_productos > 0:
            self.pct_sin_stock = (len(self.productos_sin_stock) / self.total_productos) * 100
            self.pct_stock_bajo = (len(self.productos_stock_bajo) / self.total_productos) * 100
            self.pct_stock_saludable = ((len(self.productos_stock_medio) + len(self.productos_stock_alto)) / self.total_productos) * 100
        else:
            self.pct_sin_stock = 0
            self.pct_stock_bajo = 0
            self.pct_stock_saludable = 100
    
    def generar_alertas(self) -> List[Dict]:
        """
        Genera alertas inteligentes basadas en el análisis del inventario.
        
        Returns:
            Lista de alertas con prioridad, tipo y mensaje
        """
        alertas = []
        
        # 🔴 Alerta crítica: Productos sin stock
        if self.productos_sin_stock:
            alertas.append({
                'prioridad': 'critica',
                'tipo': 'stock_agotado',
                'icono': '🔴',
                'titulo': 'Productos Agotados',
                'mensaje': f'{len(self.productos_sin_stock)} producto(s) sin stock disponible',
                'productos': [p['nombre'] for p in self.productos_sin_stock[:5]],
                'accion_sugerida': 'Reabastecer inmediatamente para evitar pérdida de ventas'
            })
        
        # 🟠 Alerta alta: Stock bajo
        if self.productos_stock_bajo:
            alertas.append({
                'prioridad': 'alta',
                'tipo': 'stock_bajo',
                'icono': '🟠',
                'titulo': 'Stock Bajo',
                'mensaje': f'{len(self.productos_stock_bajo)} producto(s) con menos de {self.UMBRAL_STOCK_BAJO} unidades',
                'productos': [f"{p['nombre']} ({p['cantidad']} uds)" for p in self.productos_stock_bajo[:5]],
                'accion_sugerida': 'Planificar reabastecimiento en los próximos días'
            })
        
        # 🟡 Alerta media: Alto porcentaje de stock bajo
        if self.pct_stock_bajo > 30:
            alertas.append({
                'prioridad': 'media',
                'tipo': 'tendencia_negativa',
                'icono': '🟡',
                'titulo': 'Tendencia de Stock Bajo',
                'mensaje': f'{self.pct_stock_bajo:.1f}% del inventario tiene stock bajo',
                'accion_sugerida': 'Revisar estrategia de reabastecimiento general'
            })
        
        # 🟢 Información: Inventario saludable
        if self.pct_stock_saludable > 80:
            alertas.append({
                'prioridad': 'info',
                'tipo': 'inventario_saludable',
                'icono': '🟢',
                'titulo': 'Inventario Saludable',
                'mensaje': f'{self.pct_stock_saludable:.1f}% del inventario tiene niveles adecuados',
                'accion_sugerida': 'Mantener monitoreo regular'
            })
        
        # 💰 Alerta de valor: Inventario de alto valor
        if self.valor_total > self.UMBRAL_VALOR_ALTO:
            alertas.append({
                'prioridad': 'info',
                'tipo': 'valor_alto',
                'icono': '💰',
                'titulo': 'Inventario de Alto Valor',
                'mensaje': f'Valor total del inventario: ${self.valor_total:,.0f} COP',
                'accion_sugerida': 'Considerar medidas de seguridad adicionales'
            })
        
        # Ordenar por prioridad
        orden_prioridad = {'critica': 0, 'alta': 1, 'media': 2, 'info': 3}
        alertas.sort(key=lambda x: orden_prioridad.get(x['prioridad'], 4))
        
        return alertas
    
    def generar_resumen_ejecutivo(self) -> str:
        """
        Genera un resumen ejecutivo inteligente del inventario.
        
        Returns:
            Texto con el resumen ejecutivo
        """
        fecha_str = self.fecha_analisis.strftime('%d de %B de %Y')
        hora_str = self.fecha_analisis.strftime('%H:%M')
        
        # Determinar estado general
        if self.pct_sin_stock > 20:
            estado = "CRÍTICO ⚠️"
            recomendacion = "Se requiere acción inmediata de reabastecimiento."
        elif self.pct_stock_bajo > 30:
            estado = "REQUIERE ATENCIÓN 🟡"
            recomendacion = "Se recomienda revisar niveles de stock próximamente."
        else:
            estado = "SALUDABLE 🟢"
            recomendacion = "El inventario se encuentra en niveles adecuados."
        
        resumen = f"""
📊 RESUMEN EJECUTIVO DE INVENTARIO
═══════════════════════════════════════
Empresa: {self.empresa.get('nombre', 'N/A')}
NIT: {self.empresa.get('nit', 'N/A')}
Fecha de análisis: {fecha_str} a las {hora_str}

📦 MÉTRICAS PRINCIPALES
───────────────────────
• Total de productos: {self.total_productos}
• Total de unidades: {self.total_unidades:,}
• Valor del inventario: ${float(self.valor_total):,.0f} COP

📈 DISTRIBUCIÓN DE STOCK
────────────────────────
• Sin stock: {len(self.productos_sin_stock)} ({self.pct_sin_stock:.1f}%)
• Stock bajo (≤10): {len(self.productos_stock_bajo)} ({self.pct_stock_bajo:.1f}%)
• Stock saludable: {len(self.productos_stock_medio) + len(self.productos_stock_alto)} ({self.pct_stock_saludable:.1f}%)

🎯 ESTADO GENERAL: {estado}
{recomendacion}

🤖 Análisis generado automáticamente por Lite Thinking IA
"""
        return resumen.strip()
    
    def generar_recomendaciones(self) -> List[Dict]:
        """
        Genera recomendaciones inteligentes basadas en el análisis.
        
        Returns:
            Lista de recomendaciones con prioridad y detalles
        """
        recomendaciones = []
        
        # Recomendaciones de reabastecimiento
        if self.productos_sin_stock:
            recomendaciones.append({
                'tipo': 'reabastecimiento_urgente',
                'prioridad': 1,
                'titulo': '🚨 Reabastecimiento Urgente',
                'descripcion': f'Los siguientes {len(self.productos_sin_stock)} productos están agotados y requieren reabastecimiento inmediato:',
                'items': [p['nombre'] for p in self.productos_sin_stock],
                'impacto': 'Alto - Pérdida potencial de ventas'
            })
        
        if self.productos_stock_bajo:
            recomendaciones.append({
                'tipo': 'reabastecimiento_planificado',
                'prioridad': 2,
                'titulo': '📋 Planificar Reabastecimiento',
                'descripcion': f'{len(self.productos_stock_bajo)} productos tienen stock bajo:',
                'items': [f"{p['nombre']} ({p['cantidad']} uds)" for p in self.productos_stock_bajo],
                'impacto': 'Medio - Riesgo de agotamiento próximo'
            })
        
        # Recomendación de optimización
        if len(self.productos_stock_alto) > self.total_productos * 0.5:
            recomendaciones.append({
                'tipo': 'optimizacion',
                'prioridad': 3,
                'titulo': '💡 Optimización de Inventario',
                'descripcion': f'{len(self.productos_stock_alto)} productos tienen stock alto. Considerar:',
                'items': [
                    'Revisar rotación de productos',
                    'Analizar costos de almacenamiento',
                    'Evaluar posibles promociones'
                ],
                'impacto': 'Bajo - Oportunidad de mejora'
            })
        
        return recomendaciones
    
    def generar_analisis_completo(self) -> Dict:
        """
        Genera el análisis completo del inventario.
        
        Returns:
            Diccionario con todos los componentes del análisis
        """
        return {
            'fecha_analisis': self.fecha_analisis.isoformat(),
            'empresa': self.empresa,
            'metricas': {
                'total_productos': self.total_productos,
                'total_unidades': self.total_unidades,
                'valor_total': float(self.valor_total),
                'pct_sin_stock': round(self.pct_sin_stock, 1),
                'pct_stock_bajo': round(self.pct_stock_bajo, 1),
                'pct_stock_saludable': round(self.pct_stock_saludable, 1),
            },
            'alertas': self.generar_alertas(),
            'resumen': self.generar_resumen_ejecutivo(),
            'recomendaciones': self.generar_recomendaciones(),
            'detalles': {
                'sin_stock': self.productos_sin_stock,
                'stock_bajo': self.productos_stock_bajo,
            }
        }


def analizar_inventario(empresa: dict, inventarios: list) -> Dict:
    """
    Función de conveniencia para analizar un inventario.
    
    Args:
        empresa: Diccionario con datos de la empresa
        inventarios: Lista de inventarios a analizar
    
    Returns:
        Diccionario con el análisis completo
    """
    analizador = AnalisisInventarioIA(empresa, inventarios)
    return analizador.generar_analisis_completo()


def generar_resumen_para_correo(empresa: dict, inventarios: list) -> Tuple[str, List[Dict]]:
    """
    Genera resumen y alertas optimizados para incluir en correo.
    
    Returns:
        Tupla con (resumen_texto, lista_alertas)
    """
    analizador = AnalisisInventarioIA(empresa, inventarios)
    return analizador.generar_resumen_ejecutivo(), analizador.generar_alertas()


# ═══════════════════════════════════════════════════════════════
# INTEGRACIÓN CON APIs DE IA EXTERNAS (Opcional)
# ═══════════════════════════════════════════════════════════════

def generar_resumen_con_openai(empresa: dict, inventarios: list) -> str:
    """
    Genera un resumen usando OpenAI GPT (si está configurado).
    Requiere: pip install openai y OPENAI_API_KEY
    """
    if not OPENAI_DISPONIBLE:
        return "OpenAI no está disponible. Instala: pip install openai"
    
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        return "OPENAI_API_KEY no configurada"
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        # Preparar contexto
        contexto = {
            'empresa': empresa.get('nombre'),
            'total_productos': len(inventarios),
            'productos': [
                {
                    'nombre': inv.get('producto_nombre'),
                    'cantidad': inv.get('cantidad', 0)
                }
                for inv in inventarios[:20]  # Limitar para no exceder tokens
            ]
        }
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Eres un experto en gestión de inventarios. Genera un análisis breve y profesional del inventario proporcionado. Incluye alertas de stock bajo y recomendaciones."
                },
                {
                    "role": "user",
                    "content": f"Analiza este inventario: {json.dumps(contexto, ensure_ascii=False)}"
                }
            ],
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error al generar resumen con OpenAI: {str(e)}"


def generar_resumen_con_anthropic(empresa: dict, inventarios: list) -> str:
    """
    Genera un resumen usando Anthropic Claude (si está configurado).
    Requiere: pip install anthropic y ANTHROPIC_API_KEY
    """
    if not ANTHROPIC_DISPONIBLE:
        return "Anthropic no está disponible. Instala: pip install anthropic"
    
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        return "ANTHROPIC_API_KEY no configurada"
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Preparar contexto
        contexto = {
            'empresa': empresa.get('nombre'),
            'total_productos': len(inventarios),
            'productos': [
                {
                    'nombre': inv.get('producto_nombre'),
                    'cantidad': inv.get('cantidad', 0)
                }
                for inv in inventarios[:20]
            ]
        }
        
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": f"Como experto en gestión de inventarios, analiza brevemente este inventario y proporciona alertas y recomendaciones: {json.dumps(contexto, ensure_ascii=False)}"
                }
            ]
        )
        
        return message.content[0].text
        
    except Exception as e:
        return f"Error al generar resumen con Claude: {str(e)}"
