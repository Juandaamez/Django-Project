/**
 * UserBadge - Átomo para mostrar información del usuario
 * Badge visual con avatar, nombre y estado online
 */

function UserBadge({ user, size = 'md', showStatus = true, className = '' }) {
  const sizeClasses = {
    sm: 'w-8 h-8 text-xs',
    md: 'w-10 h-10 text-sm',
    lg: 'w-12 h-12 text-base',
    xl: 'w-16 h-16 text-lg',
  }

  const getInitials = (name) => {
    if (!name) return '?'
    const parts = name.trim().split(' ')
    if (parts.length >= 2) {
      return `${parts[0][0]}${parts[1][0]}`.toUpperCase()
    }
    return name.substring(0, 2).toUpperCase()
  }

  const getAvatarColor = (name) => {
    const colors = [
      'bg-gradient-to-br from-blue-500 to-cyan-500',
      'bg-gradient-to-br from-purple-500 to-pink-500',
      'bg-gradient-to-br from-green-500 to-emerald-500',
      'bg-gradient-to-br from-orange-500 to-amber-500',
      'bg-gradient-to-br from-red-500 to-rose-500',
    ]
    const index = name ? name.charCodeAt(0) % colors.length : 0
    return colors[index]
  }

  if (!user) return null

  const displayName = user.first_name || user.username || user.email?.split('@')[0] || 'Usuario'
  const initials = getInitials(displayName)
  const colorClass = getAvatarColor(displayName)

  return (
    <div className={`relative inline-flex items-center gap-0 ${className}`}>
      {/* Avatar con gradiente */}
      <div
        className={`
          ${sizeClasses[size]}
          ${colorClass}
          rounded-full 
          flex items-center justify-center
          font-bold text-white
          shadow-lg shadow-brand-primary/20
          ring-2 ring-white/10
          transition-all duration-300
          hover:scale-105 hover:ring-brand-primary/50
        `}
      >
        {initials}
      </div>

      {/* Indicador de estado online */}
      {showStatus && (
        <div className="absolute -bottom-0.5 -right-0.5 flex items-center justify-center">
          <span className="relative flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500 ring-2 ring-slate-950"></span>
          </span>
        </div>
      )}
    </div>
  )
}

export default UserBadge
