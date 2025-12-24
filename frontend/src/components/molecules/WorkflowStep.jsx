import Tag from '../atoms/Tag'

function WorkflowStep({ index, badge, title, copy }) {
  const stepNumber = String(index + 1).padStart(2, '0')

  return (
    <li className="flex items-start gap-4">
      <span className="text-3xl font-display text-brand-primary/70">{stepNumber}</span>
      <div>
        <Tag variant="outline" className="border-brand-secondary/40 text-brand-secondary">
          {badge}
        </Tag>
        <h4 className="mt-2 text-xl font-semibold text-white">{title}</h4>
        <p className="text-sm text-slate-300">{copy}</p>
      </div>
    </li>
  )
}

export default WorkflowStep
