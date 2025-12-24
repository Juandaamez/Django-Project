import Tag from '../atoms/Tag'
import BulletPoint from '../atoms/BulletPoint'

function RoadmapCard({ eyebrow, title, description, bullets = [] }) {
  return (
    <div className="glass-panel">
      {eyebrow && (
        <p className="text-sm uppercase tracking-[0.3em] text-brand-primary">
          {eyebrow}
        </p>
      )}
      <h2 className="mt-3 text-2xl font-display text-white">{title}</h2>
      <p className="mt-3 text-sm text-slate-300">{description}</p>
      <ul className="mt-4 space-y-3 text-sm text-slate-200">
        {bullets.map((bullet) => (
          <BulletPoint key={bullet.text} variant={bullet.variant}>
            {bullet.text}
          </BulletPoint>
        ))}
      </ul>
      <div className="mt-4 flex flex-wrap gap-3">
        <Tag variant="outline" className="border-brand-secondary/40 text-brand-secondary">
          IA + Blockchain
        </Tag>
        <Tag variant="outline" className="border-brand-accent/50 text-brand-accent">
          PDF seguro
        </Tag>
      </div>
    </div>
  )
}

export default RoadmapCard
