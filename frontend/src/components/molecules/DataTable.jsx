/**
 * DataTable Molecule - Tabla de datos con diseño moderno
 * Soporta ordenamiento, selección y acciones
 */
import Spinner from '../atoms/Spinner'
import EmptyState from '../atoms/EmptyState'

const DataTable = ({
  columns,
  data = [],
  isLoading = false,
  emptyState,
  onRowClick,
  selectedRow,
  className = '',
}) => {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-16">
        <Spinner size="lg" className="text-brand-primary" />
      </div>
    )
  }

  if (!data.length) {
    return (
      emptyState || (
        <EmptyState
          title="No hay datos"
          description="No se encontraron registros para mostrar"
        />
      )
    )
  }

  return (
    <div className={`overflow-hidden rounded-xl border border-white/10 ${className}`}>
      <div className="overflow-x-auto">
        <table className="w-full">
          {/* Header */}
          <thead>
            <tr className="bg-white/5 border-b border-white/10">
              {columns.map((column, index) => (
                <th
                  key={column.key || index}
                  className={`
                    px-6 py-4 text-left text-xs font-semibold text-white/70 uppercase tracking-wider
                    ${column.headerClassName || ''}
                  `}
                  style={{ width: column.width }}
                >
                  {column.header}
                </th>
              ))}
            </tr>
          </thead>

          {/* Body */}
          <tbody className="divide-y divide-white/5">
            {data.map((row, rowIndex) => (
              <tr
                key={row.id || row.nit || rowIndex}
                onClick={() => onRowClick?.(row)}
                className={`
                  transition-colors duration-200
                  ${onRowClick ? 'cursor-pointer' : ''}
                  ${selectedRow === (row.id || row.nit)
                    ? 'bg-brand-primary/10'
                    : 'hover:bg-white/5'
                  }
                `}
              >
                {columns.map((column, colIndex) => (
                  <td
                    key={column.key || colIndex}
                    className={`
                      px-6 py-4 text-sm text-white/90
                      ${column.cellClassName || ''}
                    `}
                  >
                    {column.render
                      ? column.render(row[column.key], row, rowIndex)
                      : row[column.key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default DataTable
