import WorkflowStep from '../molecules/WorkflowStep'

function WorkflowTimeline({ eyebrow, title, ctaLabel, ctaHref, steps = [] }) {
  return (
    <section className="glass-panel">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          {eyebrow && (
            <p className="text-xs uppercase tracking-[0.4em] text-brand-secondary/80">
              {eyebrow}
            </p>
          )}
          <h3 className="mt-2 text-2xl font-display text-white">{title}</h3>
        </div>
        {ctaLabel && (
          <a href={ctaHref} className="text-sm font-semibold text-brand-primary">
            {ctaLabel}
          </a>
        )}
      </div>
      <ol className="mt-6 space-y-6">
        {steps.map((step, index) => (
          <WorkflowStep key={step.title} index={index} {...step} />
        ))}
      </ol>
    </section>
  )
}

export default WorkflowTimeline
