import Button from '../atoms/Button'
import Tag from '../atoms/Tag'
import RoadmapCard from '../molecules/RoadmapCard'

function HeroSection({ eyebrow, title, description, buttons = [], roadmap }) {
  return (
    <header className="grid gap-8 lg:grid-cols-[3fr,2fr]">
      <div className="space-y-6">
        {eyebrow && (
          <Tag className="text-brand-secondary">{eyebrow}</Tag>
        )}
        <h1 className="text-4xl font-display leading-tight text-white sm:text-5xl">
          {title}
        </h1>
        <p className="max-w-2xl text-base text-slate-300">{description}</p>
        <div className="flex flex-wrap gap-3">
          {buttons.map((button) => (
            <Button
              key={button.label}
              variant={button.variant}
              as={button.as}
              href={button.href}
            >
              {button.label}
            </Button>
          ))}
        </div>
      </div>

      {roadmap && <RoadmapCard {...roadmap} />}
    </header>
  )
}

export default HeroSection
