import Tag from '../atoms/Tag'
import BulletPoint from '../atoms/BulletPoint'

function SectionCard({ tag, title, description, actions = [] }) {
  return (
    <article className="glass-panel group transition-transform duration-200 hover:-translate-y-1">
      <Tag className="text-brand-primary/90">{tag}</Tag>
      <h3 className="mt-4 text-2xl font-display text-white">{title}</h3>
      <p className="mt-2 text-sm text-slate-300">{description}</p>
      <ul className="mt-5 space-y-2">
        {actions.map((action) => (
          <BulletPoint key={action}>{action}</BulletPoint>
        ))}
      </ul>
    </article>
  )
}

export default SectionCard
