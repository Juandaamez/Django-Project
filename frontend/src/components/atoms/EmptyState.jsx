/**
 * EmptyState Atom - Estado vacío para cuando no hay datos
 */

const EmptyState = ({
  icon,
  title = 'No hay datos',
  description = 'No se encontraron registros',
  action,
  className = '',
}) => {
  return (
    <div className={`flex flex-col items-center justify-center py-16 px-4 ${className}`}>
      {/* Icono */}
      <div className="w-20 h-20 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center mb-6">
        {icon || (
          <svg
            className="w-10 h-10 text-white/40"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"
            />
          </svg>
        )}
      </div>

      {/* Título */}
      <h3 className="text-xl font-display font-bold text-white mb-2">
        {title}
      </h3>

      {/* Descripción */}
      <p className="text-white/60 text-center max-w-md mb-6">
        {description}
      </p>

      {/* Acción opcional */}
      {action && (
        <div>{action}</div>
      )}
    </div>
  )
}

export default EmptyState
