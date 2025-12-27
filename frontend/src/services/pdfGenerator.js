/**
 * Generador de PDF Profesional para Inventario
 * Diseño: Moderno, Minimalista y Profesional
 * 
 * Características:
 * - Header elegante con branding corporativo
 * - Tarjetas de estadísticas con diseño limpio
 * - Barra de distribución visual
 * - Tabla de inventario con estados coloreados
 * - Footer profesional con paginación
 */
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'

// ═══════════════════════════════════════════════════════════════
// PALETA DE COLORES - Diseño Minimalista Profesional
// ═══════════════════════════════════════════════════════════════
const COLORS = {
  // Colores principales
  primary: [15, 23, 42],         // #0F172A - Slate 900 (Header)
  primaryLight: [30, 41, 59],    // #1E293B - Slate 800
  accent: [99, 102, 241],        // #6366F1 - Indigo 500
  accentLight: [129, 140, 248],  // #818CF8 - Indigo 400
  
  // Estados
  success: [16, 185, 129],       // #10B981 - Emerald 500
  successLight: [209, 250, 229], // #D1FAE5 - Emerald 100
  warning: [245, 158, 11],       // #F59E0B - Amber 500
  warningLight: [254, 243, 199], // #FEF3C7 - Amber 100
  danger: [239, 68, 68],         // #EF4444 - Red 500
  dangerLight: [254, 226, 226],  // #FEE2E2 - Red 100
  
  // Neutros
  textPrimary: [15, 23, 42],     // #0F172A
  textSecondary: [71, 85, 105],  // #475569
  textMuted: [148, 163, 184],    // #94A3B8
  border: [226, 232, 240],       // #E2E8F0
  bgLight: [248, 250, 252],      // #F8FAFC
  white: [255, 255, 255]
}

// ═══════════════════════════════════════════════════════════════
// UTILIDADES
// ═══════════════════════════════════════════════════════════════

/**
 * Formatea moneda en formato colombiano
 */
const formatCurrency = (value) => {
  try {
    return '$' + Number(value).toLocaleString('es-CO', { maximumFractionDigits: 0 })
  } catch {
    return '$0'
  }
}

/**
 * Obtiene el estado y color según la cantidad
 */
const getStockStatus = (cantidad) => {
  if (cantidad === 0) {
    return { text: 'SIN STOCK', color: COLORS.danger, bgColor: COLORS.dangerLight }
  } else if (cantidad <= 10) {
    return { text: 'STOCK BAJO', color: COLORS.warning, bgColor: COLORS.warningLight }
  }
  return { text: 'DISPONIBLE', color: COLORS.success, bgColor: COLORS.successLight }
}

/**
 * Dibuja un rectángulo redondeado
 */
const roundedRect = (doc, x, y, width, height, radius = 3, mode = 'F') => {
  doc.roundedRect(x, y, width, height, radius, radius, mode)
}

// ═══════════════════════════════════════════════════════════════
// HEADER
// ═══════════════════════════════════════════════════════════════

const drawHeader = (doc, empresa, pageWidth) => {
  const headerHeight = 75
  
  // Fondo principal del header
  doc.setFillColor(...COLORS.primary)
  doc.rect(0, 0, pageWidth, headerHeight, 'F')
  
  // Línea de acento superior (gradiente simulado)
  doc.setFillColor(...COLORS.accent)
  doc.rect(0, 0, pageWidth, 2.5, 'F')
  
  // Logo / Marca
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(9)
  doc.setTextColor(...COLORS.white)
  doc.text('LITE THINKING', 20, 16)
  
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(7)
  doc.setTextColor(...COLORS.accentLight)
  doc.text('Sistema de Inventario', 20, 22)
  
  // Título principal centrado
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(22)
  doc.setTextColor(...COLORS.white)
  doc.text('REPORTE DE INVENTARIO', pageWidth / 2, 40, { align: 'center' })
  
  // Nombre de empresa
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(12)
  doc.setTextColor(...COLORS.accentLight)
  doc.text((empresa.nombre || 'N/A').toUpperCase(), pageWidth / 2, 52, { align: 'center' })
  
  // Fecha de generación
  const fecha = new Date().toLocaleDateString('es-CO', {
    day: '2-digit',
    month: 'long',
    year: 'numeric'
  })
  doc.setFontSize(7)
  doc.setTextColor(...COLORS.textMuted)
  doc.text(`Generado: ${fecha}`, pageWidth - 20, 16, { align: 'right' })
  
  // Línea decorativa inferior
  doc.setDrawColor(...COLORS.accent)
  doc.setLineWidth(1.5)
  doc.line(20, 65, pageWidth - 20, 65)
  
  return headerHeight + 10
}

// ═══════════════════════════════════════════════════════════════
// INFORMACIÓN DE EMPRESA
// ═══════════════════════════════════════════════════════════════

const drawEmpresaInfo = (doc, empresa, startY) => {
  const cardX = 20
  const cardWidth = doc.internal.pageSize.width - 40
  const cardHeight = 35
  
  // Título de sección
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(10)
  doc.setTextColor(...COLORS.textPrimary)
  doc.text('INFORMACIÓN DE LA EMPRESA', cardX, startY)
  
  const contentY = startY + 8
  
  // Fondo del card
  doc.setFillColor(...COLORS.bgLight)
  roundedRect(doc, cardX, contentY, cardWidth, cardHeight, 3)
  
  // Borde sutil
  doc.setDrawColor(...COLORS.border)
  doc.setLineWidth(0.3)
  roundedRect(doc, cardX, contentY, cardWidth, cardHeight, 3, 'S')
  
  // Contenido
  const col1X = cardX + 10
  const col2X = cardX + cardWidth / 2 + 10
  const row1Y = contentY + 12
  const row2Y = contentY + 26
  
  // Labels
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(7)
  doc.setTextColor(...COLORS.textMuted)
  doc.text('NIT', col1X, row1Y - 5)
  doc.text('TELÉFONO', col2X, row1Y - 5)
  doc.text('DIRECCIÓN', col1X, row2Y - 5)
  
  // Valores
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(9)
  doc.setTextColor(...COLORS.textPrimary)
  doc.text(empresa.nit || 'N/A', col1X, row1Y)
  doc.text(empresa.telefono || 'N/A', col2X, row1Y)
  
  const direccion = empresa.direccion || 'N/A'
  doc.text(direccion.length > 70 ? direccion.substring(0, 70) + '...' : direccion, col1X, row2Y)
  
  return contentY + cardHeight + 15
}

// ═══════════════════════════════════════════════════════════════
// ESTADÍSTICAS
// ═══════════════════════════════════════════════════════════════

const drawStatCard = (doc, x, y, width, height, value, label, color) => {
  // Fondo
  doc.setFillColor(...COLORS.bgLight)
  roundedRect(doc, x, y, width, height, 3)
  
  // Borde
  doc.setDrawColor(...COLORS.border)
  doc.setLineWidth(0.3)
  roundedRect(doc, x, y, width, height, 3, 'S')
  
  // Valor
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(18)
  doc.setTextColor(...color)
  doc.text(String(value), x + width / 2, y + height / 2, { align: 'center' })
  
  // Label
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(7)
  doc.setTextColor(...COLORS.textSecondary)
  doc.text(label, x + width / 2, y + height - 6, { align: 'center' })
}

const drawEstadisticas = (doc, inventarios, startY, pageWidth) => {
  const totalProductos = inventarios.length
  const totalUnidades = inventarios.reduce((sum, inv) => sum + (inv.cantidad || 0), 0)
  const stockAlto = inventarios.filter(inv => inv.cantidad > 10).length
  const stockBajo = inventarios.filter(inv => inv.cantidad <= 10 && inv.cantidad > 0).length
  const sinStock = inventarios.filter(inv => inv.cantidad === 0).length
  
  // Título de sección
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(10)
  doc.setTextColor(...COLORS.textPrimary)
  doc.text('RESUMEN DEL INVENTARIO', 20, startY)
  
  const cardY = startY + 8
  const cardWidth = 40
  const cardHeight = 38
  const gap = 5
  const startX = 20
  
  // Tarjetas de estadísticas
  drawStatCard(doc, startX, cardY, cardWidth, cardHeight, totalProductos, 'Productos', COLORS.accent)
  drawStatCard(doc, startX + cardWidth + gap, cardY, cardWidth, cardHeight, totalUnidades, 'Unidades', COLORS.primary)
  drawStatCard(doc, startX + (cardWidth + gap) * 2, cardY, cardWidth, cardHeight, stockAlto, 'Stock Alto', COLORS.success)
  drawStatCard(doc, startX + (cardWidth + gap) * 3, cardY, cardWidth, cardHeight, stockBajo, 'Stock Bajo', COLORS.warning)
  
  // Barra de distribución
  const barY = cardY + cardHeight + 8
  const barHeight = 8
  const barWidth = pageWidth - 40
  
  if (totalProductos > 0) {
    const pctAlto = (stockAlto / totalProductos) * barWidth
    const pctBajo = (stockBajo / totalProductos) * barWidth
    const pctSin = (sinStock / totalProductos) * barWidth
    
    let currentX = 20
    
    // Barra de stock alto
    if (pctAlto > 0) {
      doc.setFillColor(...COLORS.success)
      doc.rect(currentX, barY, pctAlto, barHeight, 'F')
      currentX += pctAlto
    }
    
    // Barra de stock bajo
    if (pctBajo > 0) {
      doc.setFillColor(...COLORS.warning)
      doc.rect(currentX, barY, pctBajo, barHeight, 'F')
      currentX += pctBajo
    }
    
    // Barra sin stock
    if (pctSin > 0) {
      doc.setFillColor(...COLORS.danger)
      doc.rect(currentX, barY, pctSin, barHeight, 'F')
    }
    
    // Leyenda
    const legendY = barY + barHeight + 6
    const legendItems = [
      { label: 'Stock Alto', color: COLORS.success },
      { label: 'Stock Bajo', color: COLORS.warning },
      { label: 'Sin Stock', color: COLORS.danger }
    ]
    
    let legendX = 20
    legendItems.forEach(item => {
      // Punto de color
      doc.setFillColor(...item.color)
      doc.circle(legendX + 2, legendY, 1.5, 'F')
      
      // Texto
      doc.setFont('helvetica', 'normal')
      doc.setFontSize(6)
      doc.setTextColor(...COLORS.textSecondary)
      doc.text(item.label, legendX + 6, legendY + 1)
      legendX += 35
    })
    
    return legendY + 10
  }
  
  return cardY + cardHeight + 15
}

// ═══════════════════════════════════════════════════════════════
// TABLA DE INVENTARIO
// ═══════════════════════════════════════════════════════════════

const drawTablaInventario = (doc, inventarios, startY, empresa, pageWidth, pageHeight) => {
  // Título de sección
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(10)
  doc.setTextColor(...COLORS.textPrimary)
  doc.text('DETALLE DEL INVENTARIO', 20, startY)
  
  // Calcular valor total
  let valorTotal = 0
  
  // Preparar datos
  const tableData = inventarios.map((inv, index) => {
    const status = getStockStatus(inv.cantidad || 0)
    
    // Extraer precio
    let precio = 0
    if (inv.producto_precios) {
      try {
        const precios = typeof inv.producto_precios === 'string' 
          ? JSON.parse(inv.producto_precios) 
          : inv.producto_precios
        precio = precios.COP || precios.USD || 0
      } catch {}
    } else if (inv.producto_precio) {
      precio = inv.producto_precio
    }
    
    valorTotal += (inv.cantidad || 0) * precio
    
    return [
      String(index + 1),
      inv.producto_codigo || '-',
      inv.producto_nombre || '-',
      String(inv.cantidad || 0),
      status.text,
      formatCurrency(precio)
    ]
  })
  
  // Agregar fila de totales
  const totalUnidades = inventarios.reduce((sum, inv) => sum + (inv.cantidad || 0), 0)
  tableData.push(['', '', 'TOTAL', String(totalUnidades), '', formatCurrency(valorTotal)])
  
  // Generar tabla
  autoTable(doc, {
    startY: startY + 6,
    head: [['#', 'CÓDIGO', 'PRODUCTO', 'CANTIDAD', 'ESTADO', 'PRECIO']],
    body: tableData,
    theme: 'plain',
    styles: {
      font: 'helvetica',
      fontSize: 8,
      cellPadding: 4,
      valign: 'middle'
    },
    headStyles: {
      fillColor: COLORS.primary,
      textColor: COLORS.white,
      fontStyle: 'bold',
      fontSize: 7,
      cellPadding: 5
    },
    alternateRowStyles: {
      fillColor: COLORS.bgLight
    },
    columnStyles: {
      0: { cellWidth: 12, halign: 'center' },
      1: { cellWidth: 28, font: 'courier', fontStyle: 'bold' },
      2: { cellWidth: 58 },
      3: { cellWidth: 22, halign: 'center', fontStyle: 'bold' },
      4: { cellWidth: 25, halign: 'center' },
      5: { cellWidth: 25, halign: 'center' }
    },
    didParseCell: function(data) {
      // Última fila (totales)
      const isLastRow = data.row.index === tableData.length - 1
      if (isLastRow && data.section === 'body') {
        data.cell.styles.fillColor = COLORS.bgLight
        data.cell.styles.fontStyle = 'bold'
        data.cell.styles.textColor = COLORS.textPrimary
      }
      
      // Colorear estados
      if (data.column.index === 4 && data.section === 'body' && !isLastRow) {
        const estado = data.cell.raw
        if (estado === 'SIN STOCK') {
          data.cell.styles.textColor = COLORS.danger
          data.cell.styles.fillColor = COLORS.dangerLight
          data.cell.styles.fontStyle = 'bold'
        } else if (estado === 'STOCK BAJO') {
          data.cell.styles.textColor = COLORS.warning
          data.cell.styles.fillColor = COLORS.warningLight
          data.cell.styles.fontStyle = 'bold'
        } else if (estado === 'DISPONIBLE') {
          data.cell.styles.textColor = COLORS.success
          data.cell.styles.fillColor = COLORS.successLight
        }
      }
    },
    didDrawPage: function(data) {
      // Footer en cada página
      drawFooter(doc, empresa, pageHeight, pageWidth, data.pageNumber)
    },
    margin: { left: 20, right: 20 }
  })
  
  return doc.lastAutoTable.finalY
}

// ═══════════════════════════════════════════════════════════════
// FOOTER
// ═══════════════════════════════════════════════════════════════

const drawFooter = (doc, empresa, pageHeight, pageWidth, pageNumber) => {
  const footerY = pageHeight - 15
  
  // Línea superior del footer
  doc.setDrawColor(...COLORS.border)
  doc.setLineWidth(0.3)
  doc.line(20, footerY, pageWidth - 20, footerY)
  
  // Texto izquierda
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(7)
  doc.setTextColor(...COLORS.textMuted)
  doc.text('Sistema de Inventario - Lite Thinking © 2025', 20, footerY + 6)
  
  // Número de página centrado
  doc.text(`Página ${pageNumber}`, pageWidth / 2, footerY + 6, { align: 'center' })
  
  // Texto derecha
  doc.text('Documento confidencial', pageWidth - 20, footerY + 6, { align: 'right' })
}

// ═══════════════════════════════════════════════════════════════
// ESTADO VACÍO
// ═══════════════════════════════════════════════════════════════

const drawEmptyState = (doc, startY, pageWidth) => {
  const centerX = pageWidth / 2
  const y = startY + 20
  
  // Fondo
  doc.setFillColor(...COLORS.bgLight)
  roundedRect(doc, 20, y - 10, pageWidth - 40, 40, 3)
  
  // Borde
  doc.setDrawColor(...COLORS.border)
  doc.setLineWidth(0.3)
  roundedRect(doc, 20, y - 10, pageWidth - 40, 40, 3, 'S')
  
  // Texto
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(10)
  doc.setTextColor(...COLORS.textMuted)
  doc.text('No hay productos registrados en el inventario', centerX, y + 10, { align: 'center' })
}

// ═══════════════════════════════════════════════════════════════
// FUNCIONES PÚBLICAS
// ═══════════════════════════════════════════════════════════════

/**
 * Genera el PDF completo del inventario
 * @param {Object} empresa - Datos de la empresa
 * @param {Array} inventarios - Lista de inventarios
 * @returns {jsPDF} Documento PDF generado
 */
export const generarPDFInventario = (empresa, inventarios = []) => {
  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a4'
  })
  
  const pageWidth = doc.internal.pageSize.width
  const pageHeight = doc.internal.pageSize.height
  
  // 1. Header
  let currentY = drawHeader(doc, empresa, pageWidth)
  
  // 2. Información de empresa
  currentY = drawEmpresaInfo(doc, empresa, currentY)
  
  // 3. Estadísticas
  currentY = drawEstadisticas(doc, inventarios, currentY, pageWidth)
  
  // 4. Tabla o estado vacío
  if (inventarios.length > 0) {
    drawTablaInventario(doc, inventarios, currentY, empresa, pageWidth, pageHeight)
  } else {
    drawEmptyState(doc, currentY, pageWidth)
    drawFooter(doc, empresa, pageHeight, pageWidth, 1)
  }
  
  return doc
}

/**
 * Descarga el PDF del inventario
 */
export const descargarPDFInventario = (empresa, inventarios = []) => {
  const doc = generarPDFInventario(empresa, inventarios)
  const fileName = `Inventario_${empresa.nombre.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`
  doc.save(fileName)
  return fileName
}

/**
 * Obtiene el PDF como Blob
 */
export const obtenerPDFBlob = (empresa, inventarios = []) => {
  const doc = generarPDFInventario(empresa, inventarios)
  return doc.output('blob')
}

/**
 * Obtiene el PDF como Base64
 */
export const obtenerPDFBase64 = (empresa, inventarios = []) => {
  const doc = generarPDFInventario(empresa, inventarios)
  return doc.output('datauristring').split(',')[1]
}

export default {
  generarPDFInventario,
  descargarPDFInventario,
  obtenerPDFBlob,
  obtenerPDFBase64
}
