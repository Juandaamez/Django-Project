/**
 * SearchBar Atom - Barra de búsqueda con estilo moderno
 */
import { useState, useEffect } from 'react'

const SearchBar = ({
  value = '',
  onChange,
  onSearch,
  placeholder = 'Buscar...',
  debounceMs = 300,
  className = '',
}) => {
  const [internalValue, setInternalValue] = useState(value)

  // Debounce para búsqueda automática
  useEffect(() => {
    const timer = setTimeout(() => {
      if (onSearch && internalValue !== value) {
        onSearch(internalValue)
      }
    }, debounceMs)

    return () => clearTimeout(timer)
  }, [internalValue, debounceMs, onSearch, value])

  // Sincronizar con valor externo
  useEffect(() => {
    setInternalValue(value)
  }, [value])

  const handleChange = (e) => {
    const newValue = e.target.value
    setInternalValue(newValue)
    if (onChange) {
      onChange(newValue)
    }
  }

  const handleClear = () => {
    setInternalValue('')
    if (onChange) onChange('')
    if (onSearch) onSearch('')
  }

  return (
    <div className={`relative ${className}`}>
      {/* Icono de búsqueda */}
      <div className="absolute left-4 top-1/2 -translate-y-1/2 text-white/40">
        <svg
          className="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
      </div>

      <input
        type="text"
        value={internalValue}
        onChange={handleChange}
        placeholder={placeholder}
        className="w-full pl-12 pr-10 py-3 rounded-xl bg-white/5 border border-white/10 text-white placeholder-white/40 focus:outline-none focus:border-brand-primary focus:ring-2 focus:ring-brand-primary/20 transition-all duration-300"
      />

      {/* Botón para limpiar */}
      {internalValue && (
        <button
          onClick={handleClear}
          className="absolute right-3 top-1/2 -translate-y-1/2 p-1 rounded-full text-white/40 hover:text-white hover:bg-white/10 transition-colors"
          aria-label="Limpiar búsqueda"
        >
          <svg
            className="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      )}
    </div>
  )
}

export default SearchBar
