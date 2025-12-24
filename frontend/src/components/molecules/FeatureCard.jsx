/**
 * FeatureCard Molecule - Tarjeta de característica con ícono
 */

const FeatureCard = ({ icon: Icon, title, description, className = '' }) => {
  return (
    <div
      className={`
        group p-4 rounded-xl
        bg-white/5 backdrop-blur-sm
        border border-white/10 hover:border-brand-primary/30
        transition-all duration-300
        hover:bg-white/[0.07]
        ${className}
      `}
    >
      <div className="flex items-start gap-4">
        {Icon && (
          <div className="flex-shrink-0 p-2 rounded-lg bg-brand-primary/10 text-brand-primary group-hover:scale-110 transition-transform duration-300">
            <Icon className="w-5 h-5" />
          </div>
        )}
        <div>
          <h3 className="font-semibold text-white text-sm mb-1">{title}</h3>
          <p className="text-white/60 text-xs leading-relaxed">{description}</p>
        </div>
      </div>
    </div>
  )
}

export default FeatureCard
