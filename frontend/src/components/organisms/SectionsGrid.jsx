import SectionCard from '../molecules/SectionCard'

function SectionsGrid({ sections = [] }) {
  return (
    <section className="grid gap-6 md:grid-cols-2">
      {sections.map((section) => (
        <SectionCard key={section.tag} {...section} />
      ))}
    </section>
  )
}

export default SectionsGrid
