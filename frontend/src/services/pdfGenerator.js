/**
 * Generador de PDF Profesional para Inventario
 * Diseño moderno con gradientes, gráficos y estadísticas
 * 
 * Este servicio genera PDFs creativos y profesionales con:
 * - Header con branding y datos de empresa
 * - Estadísticas visuales del inventario
 * - Tabla de productos con estilos modernos
 * - Footer con información de contacto
 * - Gráfico de distribución de stock
 */
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'

// Colores del tema (brand colors)
const COLORS = {
  primary: [99, 102, 241],      // #6366F1 - Indigo
  primaryDark: [79, 70, 229],   // #4F46E5
  secondary: [139, 92, 246],    // #8B5CF6 - Purple
  success: [34, 197, 94],       // #22C55E
  warning: [245, 158, 11],      // #F59E0B
  danger: [239, 68, 68],        // #EF4444
  dark: [15, 23, 42],           // #0F172A - Slate 900
  gray: [100, 116, 139],        // #64748B
  lightGray: [241, 245, 249],   // #F1F5F9
  white: [255, 255, 255]
}

/**
 * Dibuja un rectángulo redondeado
 */
const roundedRect = (doc, x, y, width, height, radius, fill = true) => {
  doc.setLineWidth(0.5)
  doc.roundedRect(x, y, width, height, radius, radius, fill ? 'F' : 'S')
}

/**
 * Dibuja el header del PDF con diseño moderno
 */
const drawHeader = (doc, empresa, pageWidth) => {
  // Fondo del header con gradiente simulado
  doc.setFillColor(...COLORS.dark)
  doc.rect(0, 0, pageWidth, 60, 'F')
  
  // Decoración superior
  doc.setFillColor(...COLORS.primary)
  doc.rect(0, 0, pageWidth, 4, 'F')
  
  // Círculos decorativos
  doc.setFillColor(255, 255, 255, 0.1)
  doc.circle(pageWidth - 30, 30, 40, 'F')
  doc.circle(pageWidth - 60, 50, 25, 'F')
  
  // Icono de inventario (cuadrado con símbolo)
  doc.setFillColor(...COLORS.primary)
  roundedRect(doc, 15, 15, 35, 35, 4)
  
  // Símbolo de caja dentro del icono
  doc.setDrawColor(...COLORS.white)
  doc.setLineWidth(1.5)
  doc.line(22, 28, 42, 28)
  doc.line(22, 28, 22, 43)
  doc.line(42, 28, 42, 43)
  doc.line(22, 43, 42, 43)
  doc.line(22, 28, 32, 22)
  doc.line(42, 28, 32, 22)
  doc.line(32, 22, 32, 37)
  doc.line(22, 35, 32, 35)
  doc.line(42, 35, 32, 35)
  
  // Título
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(22)
  doc.setTextColor(...COLORS.white)
  doc.text('REPORTE DE INVENTARIO', 58, 28)
  
  // Subtítulo con nombre de empresa
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(12)
  doc.setTextColor(180, 180, 200)
  doc.text(empresa.nombre.toUpperCase(), 58, 40)
  
  // Fecha de generación
  doc.setFontSize(9)
  doc.setTextColor(140, 140, 160)
  const fecha = new Date().toLocaleDateString('es-CO', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
  doc.text(`Generado: ${fecha}`, 58, 50)
}

/**
 * Dibuja la sección de información de la empresa
 */
const drawEmpresaInfo = (doc, empresa, startY) => {
  const cardY = startY
  const cardHeight = 45
  
  // Card de empresa
  doc.setFillColor(...COLORS.lightGray)
  roundedRect(doc, 15, cardY, 180, cardHeight, 4)
  
  // Barra lateral decorativa
  doc.setFillColor(...COLORS.primary)
  roundedRect(doc, 15, cardY, 4, cardHeight, 2)
  
  // Título de sección
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(11)
  doc.setTextColor(...COLORS.dark)
  doc.text('INFORMACIÓN DE LA EMPRESA', 25, cardY + 12)
  
  // Datos de la empresa
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(10)
  doc.setTextColor(...COLORS.gray)
  
  const col1X = 25
  const col2X = 110
  const row1Y = cardY + 24
  const row2Y = cardY + 36
  
  // NIT
  doc.setFont('helvetica', 'bold')
  doc.setTextColor(...COLORS.dark)
  doc.text('NIT:', col1X, row1Y)
  doc.setFont('helvetica', 'normal')
  doc.setTextColor(...COLORS.gray)
  doc.text(empresa.nit, col1X + 20, row1Y)
  
  // Teléfono
  doc.setFont('helvetica', 'bold')
  doc.setTextColor(...COLORS.dark)
  doc.text('Tel:', col2X, row1Y)
  doc.setFont('helvetica', 'normal')
  doc.setTextColor(...COLORS.gray)
  doc.text(empresa.telefono || 'N/A', col2X + 18, row1Y)
  
  // Dirección
  doc.setFont('helvetica', 'bold')
  doc.setTextColor(...COLORS.dark)
  doc.text('Dirección:', col1X, row2Y)
  doc.setFont('helvetica', 'normal')
  doc.setTextColor(...COLORS.gray)
  const direccion = empresa.direccion || 'N/A'
  doc.text(direccion.substring(0, 60) + (direccion.length > 60 ? '...' : ''), col1X + 35, row2Y)
  
  return cardY + cardHeight + 10
}

/**
 * Dibuja las estadísticas del inventario con diseño de tarjetas
 */
const drawEstadisticas = (doc, inventarios, startY, pageWidth) => {
  const totalProductos = inventarios.length
  const totalUnidades = inventarios.reduce((sum, inv) => sum + (inv.cantidad || 0), 0)
  const stockBajo = inventarios.filter(inv => inv.cantidad <= 10 && inv.cantidad > 0).length
  const sinStock = inventarios.filter(inv => inv.cantidad === 0).length
  const stockAlto = inventarios.filter(inv => inv.cantidad > 10).length
  
  // Promedio de stock
  const promedioStock = totalProductos > 0 ? Math.round(totalUnidades / totalProductos) : 0
  
  // Título de sección
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(12)
  doc.setTextColor(...COLORS.dark)
  doc.text('📊 RESUMEN DEL INVENTARIO', 15, startY)
  
  const cardsY = startY + 8
  const cardWidth = 42
  const cardHeight = 40
  const gap = 4
  
  const stats = [
    { label: 'Productos', value: totalProductos, color: COLORS.primary, icon: '📦' },
    { label: 'Unidades', value: totalUnidades.toLocaleString(), color: COLORS.secondary, icon: '🏷️' },
    { label: 'Stock Alto', value: stockAlto, color: COLORS.success, icon: '✅' },
    { label: 'Stock Bajo', value: stockBajo, color: COLORS.warning, icon: '⚠️' },
  ]
  
  stats.forEach((stat, index) => {
    const x = 15 + (cardWidth + gap) * index
    
    // Fondo de la tarjeta
    doc.setFillColor(...COLORS.white)
    roundedRect(doc, x, cardsY, cardWidth, cardHeight, 4)
    
    // Borde de la tarjeta
    doc.setDrawColor(230, 230, 235)
    doc.setLineWidth(0.5)
    doc.roundedRect(x, cardsY, cardWidth, cardHeight, 4, 4, 'S')
    
    // Línea superior con color
    doc.setFillColor(...stat.color)
    roundedRect(doc, x, cardsY, cardWidth, 3, 2)
    doc.rect(x, cardsY + 2, cardWidth, 2, 'F')
    
    // Icono
    doc.setFontSize(14)
    doc.text(stat.icon, x + 5, cardsY + 16)
    
    // Valor
    doc.setFont('helvetica', 'bold')
    doc.setFontSize(16)
    doc.setTextColor(...COLORS.dark)
    doc.text(String(stat.value), x + 5, cardsY + 30)
    
    // Label
    doc.setFont('helvetica', 'normal')
    doc.setFontSize(7)
    doc.setTextColor(...COLORS.gray)
    doc.text(stat.label, x + 5, cardsY + 37)
  })
  
  return cardsY + cardHeight + 12
}

/**
 * Dibuja un mini gráfico de barras para la distribución del stock
 */
const drawStockChart = (doc, inventarios, startY, pageWidth) => {
  const chartWidth = 80
  const chartHeight = 35
  const chartX = pageWidth - chartWidth - 15
  
  const stockAlto = inventarios.filter(inv => inv.cantidad > 10).length
  const stockBajo = inventarios.filter(inv => inv.cantidad <= 10 && inv.cantidad > 0).length
  const sinStock = inventarios.filter(inv => inv.cantidad === 0).length
  const total = inventarios.length || 1
  
  // Fondo del chart
  doc.setFillColor(...COLORS.lightGray)
  roundedRect(doc, chartX - 5, startY - 45, chartWidth + 10, chartHeight + 15, 4)
  
  // Título
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(8)
  doc.setTextColor(...COLORS.dark)
  doc.text('Distribución', chartX, startY - 37)
  
  const barWidth = 18
  const maxBarHeight = 25
  const barY = startY - 8
  
  const bars = [
    { label: 'Alto', value: stockAlto, color: COLORS.success },
    { label: 'Bajo', value: stockBajo, color: COLORS.warning },
    { label: 'Sin', value: sinStock, color: COLORS.danger },
  ]
  
  bars.forEach((bar, index) => {
    const x = chartX + index * (barWidth + 5)
    const height = total > 0 ? (bar.value / total) * maxBarHeight : 0
    const y = barY - height
    
    // Barra
    doc.setFillColor(...bar.color)
    if (height > 0) {
      roundedRect(doc, x, y, barWidth - 2, height, 2)
    }
    
    // Valor sobre la barra
    doc.setFont('helvetica', 'bold')
    doc.setFontSize(7)
    doc.setTextColor(...COLORS.dark)
    doc.text(String(bar.value), x + 5, y - 2)
    
    // Label debajo
    doc.setFont('helvetica', 'normal')
    doc.setFontSize(6)
    doc.setTextColor(...COLORS.gray)
    doc.text(bar.label, x + 3, barY + 6)
  })
  
  return startY
}

/**
 * Dibuja la tabla de inventario con estilo profesional
 */
const drawTablaInventario = (doc, inventarios, startY) => {
  // Título de la tabla
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(12)
  doc.setTextColor(...COLORS.dark)
  doc.text('📋 DETALLE DEL INVENTARIO', 15, startY)
  
  // Preparar datos para la tabla
  const tableData = inventarios.map((inv, index) => {
    // Determinar estado del stock
    let estado = 'Normal'
    let estadoColor = COLORS.success
    if (inv.cantidad === 0) {
      estado = 'Sin Stock'
      estadoColor = COLORS.danger
    } else if (inv.cantidad <= 10) {
      estado = 'Stock Bajo'
      estadoColor = COLORS.warning
    } else {
      estado = 'Disponible'
    }
    
    // Formatear precio si existe
    let precioInfo = '-'
    if (inv.producto_precios) {
      const precios = typeof inv.producto_precios === 'string' 
        ? JSON.parse(inv.producto_precios) 
        : inv.producto_precios
      if (precios.COP) {
        precioInfo = `$${Number(precios.COP).toLocaleString('es-CO')}`
      } else if (precios.USD) {
        precioInfo = `$${Number(precios.USD).toLocaleString('en-US')} USD`
      }
    }
    
    return [
      String(index + 1),
      inv.producto_codigo || '-',
      inv.producto_nombre || '-',
      String(inv.cantidad || 0),
      estado,
      precioInfo,
      inv.fecha_actualizacion 
        ? new Date(inv.fecha_actualizacion).toLocaleDateString('es-CO')
        : '-'
    ]
  })

  // Generar tabla con autoTable
  autoTable(doc, {
    startY: startY + 5,
    head: [['#', 'CÓDIGO', 'PRODUCTO', 'CANT.', 'ESTADO', 'PRECIO', 'ACTUALIZACIÓN']],
    body: tableData,
    theme: 'plain',
    styles: {
      font: 'helvetica',
      fontSize: 9,
      cellPadding: 4,
      lineColor: [230, 230, 235],
      lineWidth: 0.5,
    },
    headStyles: {
      fillColor: COLORS.dark,
      textColor: COLORS.white,
      fontStyle: 'bold',
      fontSize: 8,
      cellPadding: 5,
    },
    alternateRowStyles: {
      fillColor: [248, 250, 252],
    },
    columnStyles: {
      0: { cellWidth: 10, halign: 'center' },
      1: { cellWidth: 25, font: 'courier', fontStyle: 'bold' },
      2: { cellWidth: 45 },
      3: { cellWidth: 18, halign: 'center', fontStyle: 'bold' },
      4: { cellWidth: 25, halign: 'center' },
      5: { cellWidth: 30, halign: 'right' },
      6: { cellWidth: 28, halign: 'center', fontSize: 8 },
    },
    didParseCell: function(data) {
      // Colorear la columna de estado según el valor
      if (data.column.index === 4 && data.section === 'body') {
        const estado = data.cell.raw
        if (estado === 'Sin Stock') {
          data.cell.styles.textColor = COLORS.danger
          data.cell.styles.fontStyle = 'bold'
        } else if (estado === 'Stock Bajo') {
          data.cell.styles.textColor = COLORS.warning
          data.cell.styles.fontStyle = 'bold'
        } else if (estado === 'Disponible') {
          data.cell.styles.textColor = COLORS.success
        }
      }
      // Colorear cantidad si es baja
      if (data.column.index === 3 && data.section === 'body') {
        const cantidad = parseInt(data.cell.raw) || 0
        if (cantidad === 0) {
          data.cell.styles.textColor = COLORS.danger
          data.cell.styles.fontStyle = 'bold'
        } else if (cantidad <= 10) {
          data.cell.styles.textColor = COLORS.warning
          data.cell.styles.fontStyle = 'bold'
        }
      }
    },
    didDrawPage: function(data) {
      // Agregar número de página
      const pageCount = doc.internal.getNumberOfPages()
      doc.setFont('helvetica', 'normal')
      doc.setFontSize(8)
      doc.setTextColor(...COLORS.gray)
      doc.text(
        `Página ${data.pageNumber} de ${pageCount}`,
        doc.internal.pageSize.width / 2,
        doc.internal.pageSize.height - 10,
        { align: 'center' }
      )
    }
  })
  
  return doc.lastAutoTable.finalY
}

/**
 * Dibuja el footer del PDF
 */
const drawFooter = (doc, empresa, pageHeight, pageWidth) => {
  const footerY = pageHeight - 25
  
  // Línea divisoria
  doc.setDrawColor(...COLORS.lightGray)
  doc.setLineWidth(0.5)
  doc.line(15, footerY, pageWidth - 15, footerY)
  
  // Info del footer
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(8)
  doc.setTextColor(...COLORS.gray)
  
  doc.text(`${empresa.nombre} | NIT: ${empresa.nit}`, 15, footerY + 8)
  doc.text(`${empresa.direccion || ''} | Tel: ${empresa.telefono || 'N/A'}`, 15, footerY + 14)
  
  // Marca de agua / branding
  doc.setTextColor(200, 200, 210)
  doc.setFontSize(7)
  doc.text('Sistema de Inventario - Lite Thinking 2025', pageWidth - 15, footerY + 8, { align: 'right' })
  doc.text('Documento generado automáticamente', pageWidth - 15, footerY + 14, { align: 'right' })
}

/**
 * Dibuja totales finales
 */
const drawTotales = (doc, inventarios, startY, pageWidth) => {
  const totalUnidades = inventarios.reduce((sum, inv) => sum + (inv.cantidad || 0), 0)
  
  // Card de totales
  const cardX = pageWidth - 80
  const cardY = startY + 5
  
  doc.setFillColor(...COLORS.dark)
  roundedRect(doc, cardX, cardY, 65, 25, 4)
  
  doc.setFont('helvetica', 'normal')
  doc.setFontSize(9)
  doc.setTextColor(180, 180, 200)
  doc.text('TOTAL UNIDADES', cardX + 5, cardY + 10)
  
  doc.setFont('helvetica', 'bold')
  doc.setFontSize(14)
  doc.setTextColor(...COLORS.white)
  doc.text(totalUnidades.toLocaleString(), cardX + 5, cardY + 20)
  
  return cardY + 30
}

/**
 * Genera el PDF completo del inventario
 * @param {Object} empresa - Datos de la empresa
 * @param {Array} inventarios - Lista de inventarios
 * @returns {jsPDF} Documento PDF generado
 */
export const generarPDFInventario = (empresa, inventarios = []) => {
  // Crear documento PDF
  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a4'
  })
  
  const pageWidth = doc.internal.pageSize.width
  const pageHeight = doc.internal.pageSize.height
  
  // 1. Dibujar header
  drawHeader(doc, empresa, pageWidth)
  
  // 2. Dibujar información de empresa
  let currentY = drawEmpresaInfo(doc, empresa, 70)
  
  // 3. Dibujar estadísticas
  currentY = drawEstadisticas(doc, inventarios, currentY, pageWidth)
  
  // 4. Dibujar gráfico de distribución (al lado de las estadísticas)
  drawStockChart(doc, inventarios, currentY, pageWidth)
  
  // 5. Dibujar tabla de inventario
  if (inventarios.length > 0) {
    currentY = drawTablaInventario(doc, inventarios, currentY)
    
    // 6. Dibujar totales
    drawTotales(doc, inventarios, currentY, pageWidth)
  } else {
    // Mensaje cuando no hay inventario
    doc.setFont('helvetica', 'italic')
    doc.setFontSize(11)
    doc.setTextColor(...COLORS.gray)
    doc.text('No hay productos registrados en el inventario de esta empresa.', 15, currentY + 10)
  }
  
  // 7. Dibujar footer
  drawFooter(doc, empresa, pageHeight, pageWidth)
  
  return doc
}

/**
 * Descarga el PDF del inventario
 * @param {Object} empresa - Datos de la empresa
 * @param {Array} inventarios - Lista de inventarios
 */
export const descargarPDFInventario = (empresa, inventarios = []) => {
  const doc = generarPDFInventario(empresa, inventarios)
  const fileName = `Inventario_${empresa.nombre.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`
  doc.save(fileName)
  return fileName
}

/**
 * Obtiene el PDF como Blob para enviar por correo
 * @param {Object} empresa - Datos de la empresa  
 * @param {Array} inventarios - Lista de inventarios
 * @returns {Blob} Blob del PDF
 */
export const obtenerPDFBlob = (empresa, inventarios = []) => {
  const doc = generarPDFInventario(empresa, inventarios)
  return doc.output('blob')
}

/**
 * Obtiene el PDF como Base64 para enviar al servidor
 * @param {Object} empresa - Datos de la empresa
 * @param {Array} inventarios - Lista de inventarios
 * @returns {string} PDF en formato Base64
 */
export const obtenerPDFBase64 = (empresa, inventarios = []) => {
  const doc = generarPDFInventario(empresa, inventarios)
  // Eliminar el prefijo 'data:application/pdf;base64,' si existe
  const base64 = doc.output('datauristring').split(',')[1]
  return base64
}

export default {
  generarPDFInventario,
  descargarPDFInventario,
  obtenerPDFBlob,
  obtenerPDFBase64
}
